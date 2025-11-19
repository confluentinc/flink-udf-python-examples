from email_mask.email_mask import _mask_email


def test_mask_email() -> None:
    inp = "test@example.com"
    found = _mask_email(inp)
    expected = (
        "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08@example.com"
    )
    assert found == expected
