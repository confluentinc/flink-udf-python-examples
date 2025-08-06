from pyflink.table import DataTypes
from pyflink.table.udf import udf


@udf(
    input_types=[DataTypes.BIGINT(), DataTypes.BIGINT()],
    result_type=DataTypes.BIGINT(),
)
def int_add(i, j):
    return i + j
