################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
"""Handler to execute a UDF.

The general process is: Flink-side will send a **spec** with the open
call. This contains the serialization encoding used for executing this
specific UDF. Use that spec to configure serde. Then wait for invoke
calls, deserialize the args, call the UDF, and serialize the result.

"""

from __future__ import annotations

import base64
import logging
from collections.abc import Callable
from typing import Any

from confluent_function_runtime_core import Context, RequestHandler
from typing_extensions import override

from pyflink.table.udf import ScalarFunction, UserDefinedScalarFunctionWrapper

from .core.coders import ScalarFuncSerde
from .core.exceptions import CoderError, InvocationError
from .core.importer import import_udf
from .proto.api.execution_pb2 import PythonRemoteUdfSpec
from .proto.bridge import spec_to_meta

logger = logging.getLogger(__name__)

CTX_SPEC_KEY: str = "spec_base64"


def _e_from_spec(spec: PythonRemoteUdfSpec) -> _ScalarExecutor:
    udf = import_udf(spec.class_name)

    if isinstance(udf, UserDefinedScalarFunctionWrapper):
        f_types = spec_to_meta(spec)
        serde = ScalarFuncSerde.from_meta(f_types)
        f = udf._func if not isinstance(udf._func, ScalarFunction) else udf._func.eval
        return _ScalarExecutor(spec.plugin_id, spec.class_name, f, serde)

    msg = f"Unsupported function kind: {type(udf)}"
    raise TypeError(msg)


class _ScalarExecutor:
    """Logic to actually run a scalar UDF and label errors."""

    def __init__(
        self,
        plugin_id: str,
        class_name: str,
        f: Callable[..., Any],
        serde: ScalarFuncSerde[tuple[Any, ...], Any],
    ):
        self.plugin_id = plugin_id
        self.class_name = class_name
        self._f = f
        self._serde = serde

    def invoke(self, payload: bytes) -> bytes:
        try:
            args = self._serde.decode_args(payload)
        except Exception as ex:
            msg = "error decoding UDF arguments"
            raise CoderError(msg, 0) from ex

        try:
            val = self._f(*args)
        except Exception as ex:
            msg = "error calling UDF"
            raise InvocationError(msg, 0) from ex

        try:
            return self._serde.encode_result(val)
        except Exception as ex:
            msg = "error encoding UDF return value"
            raise CoderError(msg, 0) from ex


class ExecutionHandler(RequestHandler):
    _e: _ScalarExecutor | None

    def __init__(self) -> None:
        self._e = None

    @override
    def open(self, ctx: Context) -> None:
        try:
            payload = ctx.get_config_value(CTX_SPEC_KEY)
            if payload is None:
                msg = "open context did not have spec"
                raise RuntimeError(msg)

            spec = PythonRemoteUdfSpec.FromString(base64.standard_b64decode(payload))
            logger.debug(
                "Opening executor for class %s plugin_id %s",
                spec.class_name,
                spec.plugin_id,
            )
            self._e = _e_from_spec(spec)
        except Exception:
            logger.exception("An error occurred during opening")
            raise

    @override
    def handle_request(self, payload: bytes, ctx: Context) -> bytes:
        try:
            if self._e is None:
                msg = "ExecutionHandler not opened yet; can't execute UDF"
                raise RuntimeError(msg)

            logger.debug(
                "Executing class %s plugin_id %s",
                self._e.class_name,
                self._e.plugin_id,
            )
            return self._e.invoke(payload)
        except Exception:
            logger.exception("An error occurred during execution")
            raise

    @override
    def close(self, ctx: Context) -> None:
        if self._e is not None:
            logger.debug(
                "Closing executor for class %s plugin_id %s",
                self._e.class_name,
                self._e.plugin_id,
            )
            self._e = None
