from pii_mask import _mask_pii


def test_mask_pii_email() -> None:
    found = _mask_pii("Contact me at john.doe@example.com for more info")

    expected = "Contact me at **** for more info"
    assert found == expected


def test_mask_pii_phone() -> None:
    found = _mask_pii("Call me at 555-123-4567")

    expected = "Call me at ****"
    assert found == expected


def test_mask_pii_ssn() -> None:
    found = _mask_pii("My SSN is 123-45-6789")

    expected = "My SSN is ****"
    assert found == expected


def test_mask_pii_no_pii() -> None:
    text = "This is just regular text"
    assert _mask_pii(text) == text
