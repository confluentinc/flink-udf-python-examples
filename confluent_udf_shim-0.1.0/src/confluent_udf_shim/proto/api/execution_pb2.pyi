################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Input(_message.Message):
    __slots__ = ("udf", "inputOffset", "inputConstant")
    UDF_FIELD_NUMBER: _ClassVar[int]
    INPUTOFFSET_FIELD_NUMBER: _ClassVar[int]
    INPUTCONSTANT_FIELD_NUMBER: _ClassVar[int]
    udf: UserDefinedFunction
    inputOffset: int
    inputConstant: bytes
    def __init__(self, udf: _Optional[_Union[UserDefinedFunction, _Mapping]] = ..., inputOffset: _Optional[int] = ..., inputConstant: _Optional[bytes] = ...) -> None: ...

class UserDefinedFunction(_message.Message):
    __slots__ = ("payload", "inputs", "window_index", "takes_row_as_input", "is_pandas_udf")
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    WINDOW_INDEX_FIELD_NUMBER: _ClassVar[int]
    TAKES_ROW_AS_INPUT_FIELD_NUMBER: _ClassVar[int]
    IS_PANDAS_UDF_FIELD_NUMBER: _ClassVar[int]
    payload: bytes
    inputs: _containers.RepeatedCompositeFieldContainer[Input]
    window_index: int
    takes_row_as_input: bool
    is_pandas_udf: bool
    def __init__(self, payload: _Optional[bytes] = ..., inputs: _Optional[_Iterable[_Union[Input, _Mapping]]] = ..., window_index: _Optional[int] = ..., takes_row_as_input: bool = ..., is_pandas_udf: bool = ...) -> None: ...

class Schema(_message.Message):
    __slots__ = ("fields",)
    class TypeName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROW: _ClassVar[Schema.TypeName]
        TINYINT: _ClassVar[Schema.TypeName]
        SMALLINT: _ClassVar[Schema.TypeName]
        INT: _ClassVar[Schema.TypeName]
        BIGINT: _ClassVar[Schema.TypeName]
        DECIMAL: _ClassVar[Schema.TypeName]
        FLOAT: _ClassVar[Schema.TypeName]
        DOUBLE: _ClassVar[Schema.TypeName]
        DATE: _ClassVar[Schema.TypeName]
        TIME: _ClassVar[Schema.TypeName]
        TIMESTAMP: _ClassVar[Schema.TypeName]
        BOOLEAN: _ClassVar[Schema.TypeName]
        BINARY: _ClassVar[Schema.TypeName]
        VARBINARY: _ClassVar[Schema.TypeName]
        CHAR: _ClassVar[Schema.TypeName]
        VARCHAR: _ClassVar[Schema.TypeName]
        BASIC_ARRAY: _ClassVar[Schema.TypeName]
        MAP: _ClassVar[Schema.TypeName]
        MULTISET: _ClassVar[Schema.TypeName]
        LOCAL_ZONED_TIMESTAMP: _ClassVar[Schema.TypeName]
        ZONED_TIMESTAMP: _ClassVar[Schema.TypeName]
        NULL: _ClassVar[Schema.TypeName]
    ROW: Schema.TypeName
    TINYINT: Schema.TypeName
    SMALLINT: Schema.TypeName
    INT: Schema.TypeName
    BIGINT: Schema.TypeName
    DECIMAL: Schema.TypeName
    FLOAT: Schema.TypeName
    DOUBLE: Schema.TypeName
    DATE: Schema.TypeName
    TIME: Schema.TypeName
    TIMESTAMP: Schema.TypeName
    BOOLEAN: Schema.TypeName
    BINARY: Schema.TypeName
    VARBINARY: Schema.TypeName
    CHAR: Schema.TypeName
    VARCHAR: Schema.TypeName
    BASIC_ARRAY: Schema.TypeName
    MAP: Schema.TypeName
    MULTISET: Schema.TypeName
    LOCAL_ZONED_TIMESTAMP: Schema.TypeName
    ZONED_TIMESTAMP: Schema.TypeName
    NULL: Schema.TypeName
    class MapInfo(_message.Message):
        __slots__ = ("key_type", "value_type")
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
        key_type: Schema.FieldType
        value_type: Schema.FieldType
        def __init__(self, key_type: _Optional[_Union[Schema.FieldType, _Mapping]] = ..., value_type: _Optional[_Union[Schema.FieldType, _Mapping]] = ...) -> None: ...
    class TimeInfo(_message.Message):
        __slots__ = ("precision",)
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        precision: int
        def __init__(self, precision: _Optional[int] = ...) -> None: ...
    class TimestampInfo(_message.Message):
        __slots__ = ("precision",)
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        precision: int
        def __init__(self, precision: _Optional[int] = ...) -> None: ...
    class LocalZonedTimestampInfo(_message.Message):
        __slots__ = ("precision",)
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        precision: int
        def __init__(self, precision: _Optional[int] = ...) -> None: ...
    class ZonedTimestampInfo(_message.Message):
        __slots__ = ("precision",)
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        precision: int
        def __init__(self, precision: _Optional[int] = ...) -> None: ...
    class DecimalInfo(_message.Message):
        __slots__ = ("precision", "scale")
        PRECISION_FIELD_NUMBER: _ClassVar[int]
        SCALE_FIELD_NUMBER: _ClassVar[int]
        precision: int
        scale: int
        def __init__(self, precision: _Optional[int] = ..., scale: _Optional[int] = ...) -> None: ...
    class BinaryInfo(_message.Message):
        __slots__ = ("length",)
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        length: int
        def __init__(self, length: _Optional[int] = ...) -> None: ...
    class VarBinaryInfo(_message.Message):
        __slots__ = ("length",)
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        length: int
        def __init__(self, length: _Optional[int] = ...) -> None: ...
    class CharInfo(_message.Message):
        __slots__ = ("length",)
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        length: int
        def __init__(self, length: _Optional[int] = ...) -> None: ...
    class VarCharInfo(_message.Message):
        __slots__ = ("length",)
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        length: int
        def __init__(self, length: _Optional[int] = ...) -> None: ...
    class FieldType(_message.Message):
        __slots__ = ("type_name", "nullable", "collection_element_type", "map_info", "row_schema", "decimal_info", "time_info", "timestamp_info", "local_zoned_timestamp_info", "zoned_timestamp_info", "binary_info", "var_binary_info", "char_info", "var_char_info")
        TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
        NULLABLE_FIELD_NUMBER: _ClassVar[int]
        COLLECTION_ELEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
        MAP_INFO_FIELD_NUMBER: _ClassVar[int]
        ROW_SCHEMA_FIELD_NUMBER: _ClassVar[int]
        DECIMAL_INFO_FIELD_NUMBER: _ClassVar[int]
        TIME_INFO_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_INFO_FIELD_NUMBER: _ClassVar[int]
        LOCAL_ZONED_TIMESTAMP_INFO_FIELD_NUMBER: _ClassVar[int]
        ZONED_TIMESTAMP_INFO_FIELD_NUMBER: _ClassVar[int]
        BINARY_INFO_FIELD_NUMBER: _ClassVar[int]
        VAR_BINARY_INFO_FIELD_NUMBER: _ClassVar[int]
        CHAR_INFO_FIELD_NUMBER: _ClassVar[int]
        VAR_CHAR_INFO_FIELD_NUMBER: _ClassVar[int]
        type_name: Schema.TypeName
        nullable: bool
        collection_element_type: Schema.FieldType
        map_info: Schema.MapInfo
        row_schema: Schema
        decimal_info: Schema.DecimalInfo
        time_info: Schema.TimeInfo
        timestamp_info: Schema.TimestampInfo
        local_zoned_timestamp_info: Schema.LocalZonedTimestampInfo
        zoned_timestamp_info: Schema.ZonedTimestampInfo
        binary_info: Schema.BinaryInfo
        var_binary_info: Schema.VarBinaryInfo
        char_info: Schema.CharInfo
        var_char_info: Schema.VarCharInfo
        def __init__(self, type_name: _Optional[_Union[Schema.TypeName, str]] = ..., nullable: bool = ..., collection_element_type: _Optional[_Union[Schema.FieldType, _Mapping]] = ..., map_info: _Optional[_Union[Schema.MapInfo, _Mapping]] = ..., row_schema: _Optional[_Union[Schema, _Mapping]] = ..., decimal_info: _Optional[_Union[Schema.DecimalInfo, _Mapping]] = ..., time_info: _Optional[_Union[Schema.TimeInfo, _Mapping]] = ..., timestamp_info: _Optional[_Union[Schema.TimestampInfo, _Mapping]] = ..., local_zoned_timestamp_info: _Optional[_Union[Schema.LocalZonedTimestampInfo, _Mapping]] = ..., zoned_timestamp_info: _Optional[_Union[Schema.ZonedTimestampInfo, _Mapping]] = ..., binary_info: _Optional[_Union[Schema.BinaryInfo, _Mapping]] = ..., var_binary_info: _Optional[_Union[Schema.VarBinaryInfo, _Mapping]] = ..., char_info: _Optional[_Union[Schema.CharInfo, _Mapping]] = ..., var_char_info: _Optional[_Union[Schema.VarCharInfo, _Mapping]] = ...) -> None: ...
    class Field(_message.Message):
        __slots__ = ("name", "description", "type")
        NAME_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        name: str
        description: str
        type: Schema.FieldType
        def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., type: _Optional[_Union[Schema.FieldType, _Mapping]] = ...) -> None: ...
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.RepeatedCompositeFieldContainer[Schema.Field]
    def __init__(self, fields: _Optional[_Iterable[_Union[Schema.Field, _Mapping]]] = ...) -> None: ...

class TypeInfo(_message.Message):
    __slots__ = ("type_name", "collection_element_type", "row_type_info", "tuple_type_info", "map_type_info", "avro_type_info")
    class TypeName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROW: _ClassVar[TypeInfo.TypeName]
        STRING: _ClassVar[TypeInfo.TypeName]
        BYTE: _ClassVar[TypeInfo.TypeName]
        BOOLEAN: _ClassVar[TypeInfo.TypeName]
        SHORT: _ClassVar[TypeInfo.TypeName]
        INT: _ClassVar[TypeInfo.TypeName]
        LONG: _ClassVar[TypeInfo.TypeName]
        FLOAT: _ClassVar[TypeInfo.TypeName]
        DOUBLE: _ClassVar[TypeInfo.TypeName]
        CHAR: _ClassVar[TypeInfo.TypeName]
        BIG_INT: _ClassVar[TypeInfo.TypeName]
        BIG_DEC: _ClassVar[TypeInfo.TypeName]
        SQL_DATE: _ClassVar[TypeInfo.TypeName]
        SQL_TIME: _ClassVar[TypeInfo.TypeName]
        SQL_TIMESTAMP: _ClassVar[TypeInfo.TypeName]
        BASIC_ARRAY: _ClassVar[TypeInfo.TypeName]
        PRIMITIVE_ARRAY: _ClassVar[TypeInfo.TypeName]
        TUPLE: _ClassVar[TypeInfo.TypeName]
        LIST: _ClassVar[TypeInfo.TypeName]
        MAP: _ClassVar[TypeInfo.TypeName]
        PICKLED_BYTES: _ClassVar[TypeInfo.TypeName]
        OBJECT_ARRAY: _ClassVar[TypeInfo.TypeName]
        INSTANT: _ClassVar[TypeInfo.TypeName]
        AVRO: _ClassVar[TypeInfo.TypeName]
        LOCAL_DATE: _ClassVar[TypeInfo.TypeName]
        LOCAL_TIME: _ClassVar[TypeInfo.TypeName]
        LOCAL_DATETIME: _ClassVar[TypeInfo.TypeName]
        LOCAL_ZONED_TIMESTAMP: _ClassVar[TypeInfo.TypeName]
    ROW: TypeInfo.TypeName
    STRING: TypeInfo.TypeName
    BYTE: TypeInfo.TypeName
    BOOLEAN: TypeInfo.TypeName
    SHORT: TypeInfo.TypeName
    INT: TypeInfo.TypeName
    LONG: TypeInfo.TypeName
    FLOAT: TypeInfo.TypeName
    DOUBLE: TypeInfo.TypeName
    CHAR: TypeInfo.TypeName
    BIG_INT: TypeInfo.TypeName
    BIG_DEC: TypeInfo.TypeName
    SQL_DATE: TypeInfo.TypeName
    SQL_TIME: TypeInfo.TypeName
    SQL_TIMESTAMP: TypeInfo.TypeName
    BASIC_ARRAY: TypeInfo.TypeName
    PRIMITIVE_ARRAY: TypeInfo.TypeName
    TUPLE: TypeInfo.TypeName
    LIST: TypeInfo.TypeName
    MAP: TypeInfo.TypeName
    PICKLED_BYTES: TypeInfo.TypeName
    OBJECT_ARRAY: TypeInfo.TypeName
    INSTANT: TypeInfo.TypeName
    AVRO: TypeInfo.TypeName
    LOCAL_DATE: TypeInfo.TypeName
    LOCAL_TIME: TypeInfo.TypeName
    LOCAL_DATETIME: TypeInfo.TypeName
    LOCAL_ZONED_TIMESTAMP: TypeInfo.TypeName
    class MapTypeInfo(_message.Message):
        __slots__ = ("key_type", "value_type")
        KEY_TYPE_FIELD_NUMBER: _ClassVar[int]
        VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
        key_type: TypeInfo
        value_type: TypeInfo
        def __init__(self, key_type: _Optional[_Union[TypeInfo, _Mapping]] = ..., value_type: _Optional[_Union[TypeInfo, _Mapping]] = ...) -> None: ...
    class RowTypeInfo(_message.Message):
        __slots__ = ("fields",)
        class Field(_message.Message):
            __slots__ = ("field_name", "field_type")
            FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
            FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
            field_name: str
            field_type: TypeInfo
            def __init__(self, field_name: _Optional[str] = ..., field_type: _Optional[_Union[TypeInfo, _Mapping]] = ...) -> None: ...
        FIELDS_FIELD_NUMBER: _ClassVar[int]
        fields: _containers.RepeatedCompositeFieldContainer[TypeInfo.RowTypeInfo.Field]
        def __init__(self, fields: _Optional[_Iterable[_Union[TypeInfo.RowTypeInfo.Field, _Mapping]]] = ...) -> None: ...
    class TupleTypeInfo(_message.Message):
        __slots__ = ("field_types",)
        FIELD_TYPES_FIELD_NUMBER: _ClassVar[int]
        field_types: _containers.RepeatedCompositeFieldContainer[TypeInfo]
        def __init__(self, field_types: _Optional[_Iterable[_Union[TypeInfo, _Mapping]]] = ...) -> None: ...
    class AvroTypeInfo(_message.Message):
        __slots__ = ("schema",)
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        schema: str
        def __init__(self, schema: _Optional[str] = ...) -> None: ...
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    COLLECTION_ELEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROW_TYPE_INFO_FIELD_NUMBER: _ClassVar[int]
    TUPLE_TYPE_INFO_FIELD_NUMBER: _ClassVar[int]
    MAP_TYPE_INFO_FIELD_NUMBER: _ClassVar[int]
    AVRO_TYPE_INFO_FIELD_NUMBER: _ClassVar[int]
    type_name: TypeInfo.TypeName
    collection_element_type: TypeInfo
    row_type_info: TypeInfo.RowTypeInfo
    tuple_type_info: TypeInfo.TupleTypeInfo
    map_type_info: TypeInfo.MapTypeInfo
    avro_type_info: TypeInfo.AvroTypeInfo
    def __init__(self, type_name: _Optional[_Union[TypeInfo.TypeName, str]] = ..., collection_element_type: _Optional[_Union[TypeInfo, _Mapping]] = ..., row_type_info: _Optional[_Union[TypeInfo.RowTypeInfo, _Mapping]] = ..., tuple_type_info: _Optional[_Union[TypeInfo.TupleTypeInfo, _Mapping]] = ..., map_type_info: _Optional[_Union[TypeInfo.MapTypeInfo, _Mapping]] = ..., avro_type_info: _Optional[_Union[TypeInfo.AvroTypeInfo, _Mapping]] = ...) -> None: ...

class CoderInfoDescriptor(_message.Message):
    __slots__ = ("flatten_row_type", "row_type", "separated_with_end_message")
    class FlattenRowType(_message.Message):
        __slots__ = ("schema",)
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        schema: Schema
        def __init__(self, schema: _Optional[_Union[Schema, _Mapping]] = ...) -> None: ...
    class RowType(_message.Message):
        __slots__ = ("schema",)
        SCHEMA_FIELD_NUMBER: _ClassVar[int]
        schema: Schema
        def __init__(self, schema: _Optional[_Union[Schema, _Mapping]] = ...) -> None: ...
    FLATTEN_ROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEPARATED_WITH_END_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    flatten_row_type: CoderInfoDescriptor.FlattenRowType
    row_type: CoderInfoDescriptor.RowType
    separated_with_end_message: bool
    def __init__(self, flatten_row_type: _Optional[_Union[CoderInfoDescriptor.FlattenRowType, _Mapping]] = ..., row_type: _Optional[_Union[CoderInfoDescriptor.RowType, _Mapping]] = ..., separated_with_end_message: bool = ...) -> None: ...

class PythonRemoteUdfSpec(_message.Message):
    __slots__ = ("plugin_id", "class_name", "input_coder", "output_coder")
    PLUGIN_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_CODER_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CODER_FIELD_NUMBER: _ClassVar[int]
    plugin_id: str
    class_name: str
    input_coder: CoderInfoDescriptor
    output_coder: CoderInfoDescriptor
    def __init__(self, plugin_id: _Optional[str] = ..., class_name: _Optional[str] = ..., input_coder: _Optional[_Union[CoderInfoDescriptor, _Mapping]] = ..., output_coder: _Optional[_Union[CoderInfoDescriptor, _Mapping]] = ...) -> None: ...
