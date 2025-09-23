from pyflink.table import DataTypes
from pyflink.table.types import DataType
from pyflink.table.udf import udf


def _f_int_add(i: int, j: int) -> int:
    return i + j


_int_add_inp_types: list[DataType] = [
    DataTypes.BIGINT(nullable=False),
    DataTypes.BIGINT(nullable=False),
]
int_add = udf(
    _f_int_add,
    input_types=_int_add_inp_types,
    result_type=DataTypes.BIGINT(nullable=False),
)


def _f_str_concat(i: str, j: str) -> str:
    return i + j


_str_concat_inp_types: list[DataType] = [
    DataTypes.STRING(nullable=False),
    DataTypes.STRING(nullable=False),
]
str_concat = udf(
    _f_str_concat,
    input_types=_str_concat_inp_types,
    result_type=DataTypes.STRING(nullable=False),
)
