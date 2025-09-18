################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
"""Extraction handler.

Core extraction logic lives in `core.extractor`. But validation and
conversion from the core rep to the response type happens here.

"""

import logging

from confluent_function_runtime_core import Context, RequestHandler
from typing_extensions import override

from pyflink.table.types import (
    BigIntType,
    BinaryType,
    BooleanType,
    CharType,
    DataType,
    DecimalType,
    DoubleType,
    FloatType,
    IntType,
    SmallIntType,
    TinyIntType,
    VarBinaryType,
    VarCharType,
)
from pyflink.table.udf import (
    UserDefinedScalarFunctionWrapper,
)

from .core.exceptions import MetadataExtractionError
from .core.extractor import ScalarFuncMeta, extract_scalar
from .core.importer import import_udf
from .proto.api.extractor_pb2 import (
    NOT_SCALAR_FUNCTION,
    TYPE_EXTRACTION_ERROR,
    UNKNOWN,
    USER_CODE_NOT_FOUND,
    ExtractionRequest,
    ExtractionResponse,
    Signature,
)

logger = logging.getLogger(__name__)


_BASIC_TYPES = (
    CharType,
    VarCharType,
    BooleanType,
    BinaryType,
    VarBinaryType,
    DecimalType,
    TinyIntType,
    SmallIntType,
    IntType,
    BigIntType,
    FloatType,
    DoubleType,
)


def _validate_type(t: DataType) -> None:
    if not isinstance(t, _BASIC_TYPES):
        msg = f"argument / result type {t} currently not supported"
        raise MetadataExtractionError(msg, TYPE_EXTRACTION_ERROR)


def _validate_meta(meta: ScalarFuncMeta) -> None:
    for a in meta.args:
        _validate_type(a.typ)
    _validate_type(meta.result)


def _format_type(typ: DataType) -> str:
    return str(typ)


def _meta_to_response(meta: ScalarFuncMeta) -> ExtractionResponse:
    response = ExtractionResponse()
    response.function_kind = "SCALAR"
    response.is_deterministic = meta.is_deterministic
    signature = Signature(
        argumentNames=[a.name for a in meta.args],
        argumentTypes=[_format_type(a.typ) for a in meta.args],
        returnType=_format_type(meta.result),
    )
    response.signatures.extend([signature])
    return response


class ExtractionHandler(RequestHandler):
    @override
    def handle_request(self, payload: bytes, ctx: Context) -> bytes:
        try:
            request = ExtractionRequest.FromString(payload)
            logger.info(
                "Extracting meta for class %s using plugin_id %s and version %s",
                request.class_name,
                request.plugin_id,
                request.plugin_version_id,
            )
            try:
                udf = import_udf(request.class_name)
            except ImportError as ex:
                msg = f"could not find UDF {request.class_name!r}"
                raise MetadataExtractionError(msg, USER_CODE_NOT_FOUND) from ex

            try:
                if isinstance(udf, UserDefinedScalarFunctionWrapper):
                    meta = extract_scalar(request.class_name, udf)
                    logger.info(
                        "Extracted UDF args %s result %s",
                        meta.args,
                        meta.result,
                    )
                    _validate_meta(meta)
                    response = _meta_to_response(meta)
                    return response.SerializeToString()
            except TypeError as ex:
                msg = str(ex)
                raise MetadataExtractionError(msg, TYPE_EXTRACTION_ERROR) from ex

            msg = "only Python scalar UDFs are currently supported"
            raise MetadataExtractionError(msg, NOT_SCALAR_FUNCTION)
        except MetadataExtractionError as e:
            # Propagate the exceptions coming from udf extraction
            logger.exception("An error occurred during extraction")
            response = ExtractionResponse()
            response.error.error_message = e.msg
            response.error.code = e.code
            return response.SerializeToString()
        # Add exceptions coming straight from UDFs
        except Exception as e:
            logger.exception("An unknown error occurred during extraction")
            response = ExtractionResponse()
            response.error.error_message = str(e)
            response.error.code = UNKNOWN
            return response.SerializeToString()

    @override
    def open(self, ctx: Context) -> None:
        logger.info("Opening extractor")

    @override
    def close(self, ctx: Context) -> None:
        logger.info("Closing extractor")
