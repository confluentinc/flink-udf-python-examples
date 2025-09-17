################################################################################
# Copyright 2025 Confluent Inc.
################################################################################
from importlib import import_module

from pyflink.table.udf import UserDefinedFunctionWrapper


def import_udf(class_path: str) -> UserDefinedFunctionWrapper:
    try:
        mod_name, class_name = class_path.rsplit(".", 1)
    except ValueError as ex:
        msg = f"UDF class path is not `module.path.ClassName`; got {class_path!r}"
        raise ImportError(msg) from ex
    mod = import_module(mod_name)
    try:
        udf = getattr(mod, class_name)
    except AttributeError as ex:
        msg = f"UDF class {class_name!r} does not exist in module {mod_name}"
        raise ImportError(msg) from ex
    if not isinstance(udf, UserDefinedFunctionWrapper):
        msg = f"{class_path} is not a UDF subclass; is {type(udf)}"
        raise ImportError(msg)  # noqa: TRY004

    return udf
