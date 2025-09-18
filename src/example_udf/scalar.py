from pyflink.table import DataTypes
from pyflink.table.udf import udf


@udf(
    input_types=[DataTypes.BIGINT(nullable=False), DataTypes.BIGINT(nullable=False)],
    result_type=DataTypes.BIGINT(nullable=False),
)
def int_add(i: int, j: int) -> int:
    return i + j


@udf(
    input_types=[DataTypes.VARCHAR(nullable=False), DataTypes.VARCHAR(nullable=False)],
    result_type=DataTypes.VARCHAR(nullable=False),
)
def str_concat(i: str, j: str) -> str:
    return i + j
