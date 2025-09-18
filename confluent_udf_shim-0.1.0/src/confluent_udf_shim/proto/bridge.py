################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
"""This module converts from the protobuf UDF spec to core types.

The SQL types of the UDF define the wire format that will be used for "execute"
calls. The Flink operators communicate to this shim the SQL types they are
sending via `PythonRemoteUdfSpec`. This module translates those types into the
equivalent native PyFlink types, because they have convenience methods which
help with serde.

"""

from __future__ import annotations

import pyflink.table.types as table

from ..core.extractor import NamedArg, ScalarFuncMeta
from .api.execution_pb2 import PythonRemoteUdfSpec, Schema


def type_proto_to_table(pb_type: Schema.FieldType) -> table.DataType:
    if pb_type.type_name == Schema.CHAR:
        return table.CharType(  # type: ignore[no-untyped-call]
            length=pb_type.char_info.length,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.VARCHAR:
        return table.VarCharType(  # type: ignore[no-untyped-call]
            length=pb_type.var_char_info.length,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.BOOLEAN:
        return table.BooleanType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.BINARY:
        return table.BinaryType(  # type: ignore[no-untyped-call]
            length=pb_type.binary_info.length,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.VARBINARY:
        return table.VarBinaryType(  # type: ignore[no-untyped-call]
            length=pb_type.var_binary_info.length,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.TINYINT:
        return table.TinyIntType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.SMALLINT:
        return table.SmallIntType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.INT:
        return table.IntType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.BIGINT:
        return table.BigIntType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.TIME:
        return table.TimeType(  # type: ignore[no-untyped-call]
            precision=pb_type.time_info.precision,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.DATE:
        return table.DateType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.FLOAT:
        return table.FloatType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.DOUBLE:
        return table.DoubleType(nullable=pb_type.nullable)  # type: ignore[no-untyped-call]
    if pb_type.type_name == Schema.DECIMAL:
        return table.DecimalType(  # type: ignore[no-untyped-call]
            precision=pb_type.decimal_info.precision,
            scale=pb_type.decimal_info.scale,
            nullable=pb_type.nullable,
        )
    if pb_type.type_name == Schema.TIMESTAMP:
        return table.TimestampType(  # type: ignore[no-untyped-call]
            precision=pb_type.timestamp_info.precision,
            nullable=pb_type.nullable,
        )

    msg = f"type {pb_type} not supported"
    raise TypeError(msg)


def spec_to_meta(spec: PythonRemoteUdfSpec) -> ScalarFuncMeta:
    """Normalize spec into the core repr."""
    args = tuple(
        NamedArg(t.name, type_proto_to_table(t.type))
        for t in spec.input_coder.flatten_row_type.schema.fields
    )
    result = type_proto_to_table(
        spec.output_coder.flatten_row_type.schema.fields[0].type
    )
    return ScalarFuncMeta(spec.class_name, args, result, is_deterministic=False)
