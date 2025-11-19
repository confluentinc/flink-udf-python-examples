from pyflink.table import DataTypes
from pyflink.table.types import DataType
from pyflink.table.udf import udf
import hashlib


def _mask_email(email: str) -> str:
    """
    Mask the local part of an email address by hashing it with SHA256.

    Args:
        email: Email address string (e.g., "user@example.com")

    Returns:
        Masked email with hashed local part (e.g., "hash@example.com")
    """
    split_email = email.split("@")
    return (
        hashlib.sha256(split_email[0].encode("utf-8")).hexdigest()
        + "@"
        + split_email[1]
    )


_mask_email_input_types: list[DataType] = [DataTypes.STRING()]
mask_email = udf(
    _mask_email,
    input_types=_mask_email_input_types,
    result_type=DataTypes.STRING(),
)
