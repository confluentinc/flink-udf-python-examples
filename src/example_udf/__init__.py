from pyflink.table import DataTypes
from pyflink.table.udf import udf


@udf(
    input_types=[DataTypes.BIGINT(), DataTypes.BIGINT()],
    result_type=DataTypes.BIGINT(),
)
def user_add_udf(i, j):
    return i + j
