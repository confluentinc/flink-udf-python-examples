from datafog import TextPIIAnnotator
from pyflink.table.types import DataTypes, DataType
from pyflink.table.udf import udf

# Module-level annotator instance (lazy initialization)
_annotator: TextPIIAnnotator | None = None


def _get_annotator() -> TextPIIAnnotator:
    """Get or create the PII annotator instance."""
    global _annotator
    if _annotator is None:
        _annotator = TextPIIAnnotator()
    return _annotator


def _mask_pii(text: str) -> str:
    """Mask PII in the input text.

    Uses regex-based PII detection for lightweight, fast processing.
    Detects and masks:
    - Email addresses
    - Phone numbers
    - Social Security Numbers (SSN)
    - Credit card numbers
    - IP addresses
    - Dates of birth
    - ZIP codes

    Args:
        text: Input text that may contain PII

    Returns:
        Text with PII masked
    """
    annotator = _get_annotator()

    # Detect PII entities
    annotations = annotator.run(text)

    # Replace detected PII values with mask
    result = text
    for values in annotations.values():
        for val in values:
            if val:  # Skip empty strings from false positives
                result = result.replace(val, "****")

    return result


_mask_pii_input_types: list[DataType] = [DataTypes.STRING()]
mask_pii = udf(
    _mask_pii,
    input_types=_mask_pii_input_types,
    result_type=DataTypes.STRING(),
)
