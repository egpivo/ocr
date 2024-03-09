import pytest
from fastapi import HTTPException

from ocr.dependencies import extract_text_from_image, is_valid_image


@pytest.mark.usefixtures(
    "false_example_image_string", "positive_example_image_string", "expected_result"
)
def test_extract_text_from_image(
    false_example_image_string, positive_example_image_string, expected_result
):
    # Use pytest.raises to capture and assert the HTTPException for invalid image
    with pytest.raises(HTTPException) as exc_info:
        # Call the function with the invalid image string
        extract_text_from_image(false_example_image_string)

    # Check if the exception status code is 400
    assert exc_info.value.status_code == 400
    assert "Invalid image format." in str(exc_info.value.detail)

    # Test with a positive example_image_string, expecting no errors
    result = extract_text_from_image(positive_example_image_string)
    assert result == expected_result


@pytest.mark.usefixtures("positive_example_image_string", "false_example_image_string")
def test_is_valid_image(positive_example_image_string, false_example_image_string):
    assert is_valid_image(positive_example_image_string)
    assert not is_valid_image(false_example_image_string)
