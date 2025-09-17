################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
"""Execution argument and result serialization.

`ScalarFuncSerde` is the main entry point. This has methods for serde
on arguments and results.

That delegates to `_TypeSerde`, which knows how to do that for
individual types. Serialization for a SQL type is composed of two
parts:

- **Coder**, which translates between bytes-on-wire and an "internal
  type". The **internal type** is the Python representation of the
  wire encoding. The coders are re-purposed from `pyflink` (e.g.
  `FloatCoderImpl`), although some are re-implemented here to match
  the Java Flink implementations (e.g. `NullableSerializerImpl`).
  These must match what is used on the Java side in
  https://github.com/confluentinc/flink/blob/release-2.0-confluent/flink-table/flink-table-runtime/src/main/java/org/apache/flink/table/runtime/typeutils/InternalSerializers.java

- **Conversion**, which translates between the internal type and the
  PyFlink UDF Python user types. The *user type* is the user-friendly
  Python-native type which best represents the SQL type and match what
  are described in
  https://nightlies.apache.org/flink/flink-docs-release-2.1/docs/dev/python/table/python_types/
  `pyflink.table.types.DataType` subclasses have these conversions
  defined internally. We reuse the mapping defined via upstream
  `pyflink` in `DataType.from_sql_type` and `DataType.to_sql_type`
  (where `sql` in this case means the internal type).

"""

from __future__ import annotations

from abc import ABC
from typing import Any, Generic, TypeVar

from typing_extensions import override

from pyflink.fn_execution.coder_impl_slow import (
    BigIntCoderImpl,
    BinaryCoderImpl,
    BooleanCoderImpl,
    CharCoderImpl,
    DoubleCoderImpl,
    FieldCoderImpl,
    FloatCoderImpl,
    IntCoderImpl,
    SmallIntCoderImpl,
    TimestampCoderImpl,
    TinyIntCoderImpl,
)
from pyflink.fn_execution.stream_slow import InputStream, OutputStream
from pyflink.table.types import (
    BigIntType,
    BinaryType,
    BooleanType,
    CharType,
    DataType,
    DateType,
    DoubleType,
    FloatType,
    IntType,
    SmallIntType,
    TimestampType,
    TimeType,
    TinyIntType,
    VarBinaryType,
    VarCharType,
)

from ..core.extractor import ScalarFuncMeta


class NullableSerializerImpl(FieldCoderImpl):
    """Serializer which prepends a byte if the value is null."""

    # This must match encoding in
    # https://github.com/confluentinc/flink/blob/e80b6938c1e158885d8b5bed376b8124982824e2/flink-core/src/main/java/org/apache/flink/api/java/typeutils/runtime/NullableSerializer.java
    # CC Flink never uses "pad null if fixed length", so no need to
    # implement that.
    # https://github.com/confluentinc/flink/blob/10e53697eef3182ea27238be4c9bbe901fe7b4cf/cc-flink-extensions/cc-flink-udf-adapter-api/src/main/java/io/confluent/flink/udf/adapter/api/RemoteUdfSpec.java#L199

    def __init__(self, inner: FieldCoderImpl):
        self._inner = inner

    @override
    def encode_to_stream(self, value: Any | None, out_stream: OutputStream) -> None:
        if value is not None:
            out_stream.write_int8(0)
            self._inner.encode_to_stream(value, out_stream)
        else:
            out_stream.write_int8(1)

    @override
    def decode_from_stream(self, in_stream: InputStream, length: int = 0) -> Any | None:
        is_null_b = in_stream.read_int8()  # type: ignore[no-untyped-call]
        is_null = bool(is_null_b)
        if not is_null:
            return self._inner.decode_from_stream(in_stream)
        return None


def _coder_for(typ: DataType) -> FieldCoderImpl:
    """Build the coder for a SQL type."""
    inner = _inner_coder_for(typ)
    # Java side does not check if SQL type is actually nullable for
    # either arguments or result; always wraps with null wrapper.
    # https://github.com/confluentinc/flink/blob/c207ad912e2b1cd5be6c8d4d584ef7ad926b24f1/cc-flink-extensions/cc-flink-udf-adapter-api/src/main/java/io/confluent/flink/udf/adapter/api/RemoteUdfSpec.java#L182
    return NullableSerializerImpl(inner)


# This is based on
# https://github.com/confluentinc/flink/blob/3ccf825b84d2293bb19b0cf3efcaca1dd5d12a0e/flink-table/flink-table-runtime/src/main/java/org/apache/flink/table/runtime/typeutils/InternalSerializers.java#L66
def _inner_coder_for(typ: DataType) -> FieldCoderImpl:
    if isinstance(typ, (CharType, VarCharType)):
        return CharCoderImpl()
    if isinstance(typ, BooleanType):
        return BooleanCoderImpl()
    if isinstance(typ, (BinaryType, VarBinaryType)):
        return BinaryCoderImpl()
    if isinstance(typ, TinyIntType):
        return TinyIntCoderImpl()
    if isinstance(typ, SmallIntType):
        return SmallIntCoderImpl()
    if isinstance(typ, (IntType, TimeType, DateType)):
        return IntCoderImpl()
    if isinstance(typ, BigIntType):
        return BigIntCoderImpl()
    if isinstance(typ, FloatType):
        return FloatCoderImpl()
    if isinstance(typ, DoubleType):
        return DoubleCoderImpl()
    # TODO: https://confluentinc.atlassian.net/browse/FRT-1282
    # The PyFlink vendored wire format for decimal is not the same as Java.
    # if isinstance(typ, DecimalType):
    #     return DecimalCoderImpl(typ.precision, typ.scale)
    if isinstance(typ, TimestampType):
        return TimestampCoderImpl(typ.precision)  # type: ignore[no-untyped-call]

    msg = f"type {typ} not supported"
    raise TypeError(msg)


class _ArgsCoder(FieldCoderImpl):
    """UDF arguments are serialized in order."""

    # This must match the encoding Java-side in
    # https://github.com/confluentinc/flink/blob/8f39c4e3038e03fec9875501e9bd7993d20a3336/cc-flink-extensions/cc-flink-udf-adapter-api/src/main/java/io/confluent/flink/udf/adapter/api/RemoteUdfSerialization.java#L51

    def __init__(self, inners: tuple[FieldCoderImpl, ...]) -> None:
        self._inners = inners

    @override
    def encode_to_stream(
        self, value: tuple[Any, ...], out_stream: OutputStream
    ) -> None:
        for arg, coder in zip(value, self._inners, strict=True):
            coder.encode_to_stream(arg, out_stream)

    @override
    def decode_from_stream(
        self, in_stream: InputStream, length: int = 0
    ) -> tuple[Any, ...]:
        return tuple(coder.decode_from_stream(in_stream) for coder in self._inners)


class _ArgsType(DataType):
    """Shim "SQL type" which lets us serialize arguments as a value
    and handles internal to user type conversion.

    """

    def __init__(self, typs: tuple[DataType, ...]) -> None:
        super().__init__(nullable=False)  # type: ignore[no-untyped-call]
        self._typs = typs
        self._need_conversion = any(t.need_conversion() for t in self._typs)

    @override
    def need_conversion(self) -> bool:
        return self._need_conversion

    @override
    def to_sql_type(self, obj: tuple[Any, ...]) -> tuple[Any, ...]:
        if not self._need_conversion:
            return obj
        return tuple(
            t.to_sql_type(v)  # type: ignore[no-untyped-call]
            for t, v in zip(self._typs, obj, strict=True)
        )

    @override
    def from_sql_type(self, obj: tuple[Any, ...]) -> tuple[Any, ...]:
        if not self._need_conversion:
            return obj
        return tuple(
            t.from_sql_type(v)  # type: ignore[no-untyped-call]
            for t, v in zip(self._typs, obj, strict=True)
        )


T = TypeVar("T")


class _TypeSerde(ABC, Generic[T]):
    """Core serialization process for a type.

    Convert from/to user/internal, then serialize from/to
    internal/bytes.

    """

    def __init__(self, typ: DataType, coder: FieldCoderImpl) -> None:
        self._typ = typ
        self._coder = coder

    @staticmethod
    def for_type(typ: DataType) -> _TypeSerde[Any]:
        return _TypeSerde(typ, _coder_for(typ))

    @staticmethod
    def for_args(typs: tuple[DataType, ...]) -> _TypeSerde[tuple[Any, ...]]:
        return _TypeSerde(
            _ArgsType(typs),
            _ArgsCoder(tuple(_coder_for(t) for t in typs)),
        )

    def deserialize(self, stream: InputStream) -> T:
        internal = self._coder.decode_from_stream(stream)
        # Conversion handles `None`.
        return self._typ.from_sql_type(internal)  # type: ignore[no-untyped-call, no-any-return]

    def serialize(self, val: T, stream: OutputStream) -> None:
        # Conversion handles `None`.
        internal = self._typ.to_sql_type(val)  # type: ignore[no-untyped-call]
        self._coder.encode_to_stream(internal, stream)


A = TypeVar("A")
R = TypeVar("R")


class ScalarFuncSerde(Generic[A, R]):
    """Serialization specialized for scalar functions."""

    def __init__(self, arg_serde: _TypeSerde[A], result_serde: _TypeSerde[R]) -> None:
        self._arg_serde = arg_serde
        self._result_serde = result_serde

    @staticmethod
    def from_meta(meta: ScalarFuncMeta) -> ScalarFuncSerde[tuple[Any, ...], Any]:
        arg_serde = _TypeSerde.for_args(tuple(a.typ for a in meta.args))
        result_serde = _TypeSerde.for_type(meta.result)
        return ScalarFuncSerde(arg_serde, result_serde)

    def encode_args(self, args: A) -> bytes:
        stream = OutputStream()  # type: ignore[no-untyped-call]
        self._arg_serde.serialize(args, stream)
        return stream.get()

    def decode_args(self, payload: bytes) -> A:
        stream = InputStream(payload)  # type: ignore[no-untyped-call]
        args = self._arg_serde.deserialize(stream)
        remaining = stream.size()  # type: ignore[no-untyped-call]
        if remaining != 0:
            msg = (
                "argument payload was not completely consumed; "
                f"{remaining} bytes remain"
            )
            raise ValueError(msg)

        return args

    def encode_result(self, res: R) -> bytes:
        stream = OutputStream()  # type: ignore[no-untyped-call]
        self._result_serde.serialize(res, stream)
        return stream.get()

    def decode_result(self, payload: bytes) -> R:
        stream = InputStream(payload)  # type: ignore[no-untyped-call]
        result = self._result_serde.deserialize(stream)
        remaining = stream.size()  # type: ignore[no-untyped-call]
        if remaining != 0:
            msg = (
                f"result payload was not completely consumed; {remaining} bytes remain"
            )
            raise ValueError(msg)
        return result
