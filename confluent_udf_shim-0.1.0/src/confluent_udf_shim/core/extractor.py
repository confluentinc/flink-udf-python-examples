################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
"""This is the core extraction logic.

`extract_scalar` produces a canonical and **core representation**
`ScalarFuncMeta` which contains PyFlink types, because they are most
useful.

Many different places in the code base want to do something that looks
like "extraction" so it is centralized here. Different "output
formats" are created from this core rep.

- Into an `ExtractionResponse` for the extraction handler.

- Into example `PythonUdfSpec`s for execution testing.

- Parsed to produce `spec_tools` CLI helpers.

"""

import inspect
from collections.abc import Iterable
from dataclasses import dataclass

from pyflink.table.types import DataType
from pyflink.table.udf import (
    ScalarFunction,
    UserDefinedScalarFunctionWrapper,
)


@dataclass
class NamedArg:
    name: str
    typ: DataType


@dataclass
class ScalarFuncMeta:
    class_path: str
    args: tuple[NamedArg, ...]
    result: DataType
    is_deterministic: bool


def _normalize_scalar_arg_types(
    typs: list[DataType] | DataType | str | list[str] | None,
) -> Iterable[DataType]:
    """Take the variety of ways that you can specify
    `@udf(input_types)` and normalize into just `DataType`s.

    E.g. Users of upstream PyFlink are allowed to do
    `@udf(input_types=["BIGINT", "VARCHAR"])` or
    `@udf(input_types="BIGINT,VARCHAR")` or
    `@udf(input_types=[table.types.BIGINT, table.types.VARCHAR])`.

    It looks like upstream PyFlink has incorrectly generous type
    annotations on this field: no documentation says you can use a
    single `DataType` on a scalar UDF.

    """
    if typs is None:
        msg = "UDF `input_types` must be specified"
        raise TypeError(msg)

    # TODO: https://confluentinc.atlassian.net/browse/FRT-1274 support
    # "string-y" type definitions
    if not isinstance(typs, list):
        msg = f"UDF `input_types` must be a `list[DataType]`; found {type(typs)}"
        raise TypeError(msg)

    for typ in typs:
        if not isinstance(typ, DataType):
            msg = (
                "UDF `input_types` each must be a `DataType` instance; "
                f"found {type(typ)}"
            )
            raise TypeError(msg)

        yield typ


def _normalize_scalar_result_type(
    typ: list[DataType] | DataType | str | list[str] | None,
) -> DataType:
    """Take the variety of ways that you can specify
    `@udf(result_type)` and normalize into `DataType`.

    E.g. Users of upstream PyFlink are allowed to do
    `@udf(result_type="BIGINT")` or
    `@udf(result_type=table.types.BIGINT)`.

    It looks like upstream PyFlink has incorrectly generous type
    annotations on this field: no documentation says you can use a
    `list[DataType]` as a result type on a scalar UDF.

    """
    if typ is None:
        msg = "UDF `result_type` must be specified"
        raise TypeError(msg)

    # TODO: https://confluentinc.atlassian.net/browse/FRT-1274 support
    # "string-y" type definitions
    if not isinstance(typ, DataType):
        msg = (
            f"scalar UDF `result_type` must be a `DataType` instance; found {type(typ)}"
        )
        raise TypeError(msg)

    return typ


def _inspect_input_names(udf: UserDefinedScalarFunctionWrapper) -> list[str]:
    sig_func = udf._func.eval if isinstance(udf._func, ScalarFunction) else udf._func

    signature = inspect.signature(sig_func)
    return [
        param.name
        for param in signature.parameters.values()
        if param.default is inspect.Parameter.empty
    ]


def extract_scalar(
    class_path: str,
    udf: UserDefinedScalarFunctionWrapper,
) -> ScalarFuncMeta:
    arg_types = _normalize_scalar_arg_types(udf._input_types)
    arg_names = _inspect_input_names(udf)
    args = tuple(NamedArg(n, t) for n, t in zip(arg_names, arg_types, strict=True))
    result = _normalize_scalar_result_type(udf._result_type)
    return ScalarFuncMeta(
        class_path,
        args,
        result,
        is_deterministic=udf._deterministic,
    )
