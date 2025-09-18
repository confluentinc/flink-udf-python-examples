################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ErrorCode]
    GENERAL_FAILED_EXTRACTION: _ClassVar[ErrorCode]
    USER_CODE_NOT_FOUND: _ClassVar[ErrorCode]
    NOT_SCALAR_FUNCTION: _ClassVar[ErrorCode]
    NO_PUBLIC_NO_ARG_CONSTRUCTOR: _ClassVar[ErrorCode]
    TYPE_EXTRACTION_ERROR: _ClassVar[ErrorCode]
    NOT_SUPPORTED_FUNCTION: _ClassVar[ErrorCode]
    CLASS_NOT_SERIALIZABLE: _ClassVar[ErrorCode]
UNKNOWN: ErrorCode
GENERAL_FAILED_EXTRACTION: ErrorCode
USER_CODE_NOT_FOUND: ErrorCode
NOT_SCALAR_FUNCTION: ErrorCode
NO_PUBLIC_NO_ARG_CONSTRUCTOR: ErrorCode
TYPE_EXTRACTION_ERROR: ErrorCode
NOT_SUPPORTED_FUNCTION: ErrorCode
CLASS_NOT_SERIALIZABLE: ErrorCode

class Error(_message.Message):
    __slots__ = ("code", "error_message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    error_message: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class ExtractionRequest(_message.Message):
    __slots__ = ("plugin_id", "plugin_version_id", "class_name")
    PLUGIN_ID_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_VERSION_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    plugin_id: str
    plugin_version_id: str
    class_name: str
    def __init__(self, plugin_id: _Optional[str] = ..., plugin_version_id: _Optional[str] = ..., class_name: _Optional[str] = ...) -> None: ...

class Signature(_message.Message):
    __slots__ = ("argumentTypes", "returnType", "argumentNames")
    ARGUMENTTYPES_FIELD_NUMBER: _ClassVar[int]
    RETURNTYPE_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTNAMES_FIELD_NUMBER: _ClassVar[int]
    argumentTypes: _containers.RepeatedScalarFieldContainer[str]
    returnType: str
    argumentNames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, argumentTypes: _Optional[_Iterable[str]] = ..., returnType: _Optional[str] = ..., argumentNames: _Optional[_Iterable[str]] = ...) -> None: ...

class ExtractionResponse(_message.Message):
    __slots__ = ("error", "signatures", "is_deterministic", "function_kind")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    SIGNATURES_FIELD_NUMBER: _ClassVar[int]
    IS_DETERMINISTIC_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_KIND_FIELD_NUMBER: _ClassVar[int]
    error: Error
    signatures: _containers.RepeatedCompositeFieldContainer[Signature]
    is_deterministic: bool
    function_kind: str
    def __init__(self, error: _Optional[_Union[Error, _Mapping]] = ..., signatures: _Optional[_Iterable[_Union[Signature, _Mapping]]] = ..., is_deterministic: bool = ..., function_kind: _Optional[str] = ...) -> None: ...
