################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
from typing_extensions import override

from confluent_udf_shim.proto.api.extractor_pb2 import ErrorCode


class MetadataExtractionError(Exception):
    """Raised when there is an error during metadata extraction."""

    def __init__(self, message: str, code: ErrorCode):
        self.msg = message
        self.code = code

    @override
    def __str__(self) -> str:
        return f"{self.code} {self.msg}"


# TODO: Take a pass over exception handling to ensure errors are reported
# through all the way https://confluentinc.atlassian.net/browse/FRT-1279
class InvocationError(Exception):
    """Raised when customer UDF code causes an exception."""

    def __init__(self, message: str, code: int):
        self.msg = message
        self.code = code


class CoderError(Exception):
    """Raised when there is an error during serde of invoke data."""

    def __init__(self, message: str, code: int):
        self.msg = message
        self.code = code
