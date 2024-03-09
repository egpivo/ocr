import pytest
from fastapi import HTTPException

from ocr.dependencies import extract_text_from_image


@pytest.mark.usefixtures(
    "false_example_image_string", "positive_example_image_string", "expected_result"
)
def test_extract_text_from_image(
    false_example_image_string, positive_example_image_string, expected_result
):
    # Use pytest.raises to capture and assert the HTTPException
    with pytest.raises(HTTPException) as exc_info:
        # Call the function with the example image string
        extract_text_from_image(false_example_image_string)

    # Check if the exception status code is 400
    assert exc_info.value.status_code == 400

    # Optionally, check the detail message if needed
    assert "Error processing image: Incorrect padding" in str(exc_info.value)

    # Test with a positive example_image_string, expecting no errors
    result = extract_text_from_image(positive_example_image_string)

    # Check if the result matches the expected result
    assert result == expected_result
