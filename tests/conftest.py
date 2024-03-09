import pytest


@pytest.fixture
def positive_example_image_string():
    # Properly padded base64 image string
    return "iVBORw0KGgoAAAANSUhEUgAAAGcAAAAVCAYAAABbq/AzAAAACXBIWXMAAA7EAAAOxAGVKw4bAAADiUlEQVRoge3YTWgeVRQG4IcQJJQSQihBNIQiXYUSpJSgIF1IkSKllCJFQggutBQRQRfFH3RTRFwVERdBRHcuREVEupASRIP4C7VoFSmWSq2gtRGjNm21Ls79+k0mM3cmLrpxXhjm++aec973/sy55w4dOnTo0KFDhw4FLOIe3IWrmWtbwWcfLuDhinj7avzvTjyLDXp24F2cxx84gQMVdgfxHVbwFe5tqaEObXxynDCAQ/g2af+8hjM3ftcwIzoPQ5iouObEQG1INvP4PvlVBT+IYxVxhlJ7Vad6GMICHsQkNqWO/I7Zgt1s6twejGEvfhMLrI2GKjT5NHHCs6l/dyTtM8nnzkL/msbvGhbFTOdwDIfT7514GyN4ryb403glE+8JvN/AWcY8Xi/8P45HK+J+0FJDFZp8mjgHxRu1o2TzkH62aDN+YFS8tlMZQdP4S6yCMhZqgr8oVlAdtuFvDGdsyngHL6Xfw0L31pq4Qy00VCHn04bzlmSzsWQznmw2lJ7XjZ8BbMclfJ0R/CRexS8ZmzJGcb/+nnFcrJ6B1P4lroiJb8I4nhGD8FzhGZwu2Z5OHJtbaFiv7jacvTG6qWSzKdmMZbjX4D78kGnfisvYUtNeN/PDYr8Yxo2iCDiH5ws2ZxN/HY7ob8insKvQtj09Hyz5DOkXLm00rEd3G04iZR3Vn8xpkdKuWjtptW+O1HAyI/Y1vJFpzwYvYUakx17nTjb4Dor0MIH9YgPtpZxJ1emjl6YnGzTMWF2NzbTQ3ZZzRKTfc6KIOSoKiMu4oeRbO36DWK4g62GLGJTbM8LXg2/EKtuIpXRfzthfSe3LOJPub+EpkUr+ERNXTMkT6X6mQcObuLnw/NcWuttyLuGBUoxZkcovZXhWYQA/6efDMh7Hh/ikbcAGTCe+Jf38++M6/Iur7k98ZnWqk/5/oX7SexouJu7edbGF7v/KOYBH8HKGoxJjqqu1cVES5g5s1L+Wh3GbyNvjYm+5oH+QnEq8oxW+t4rSfkqkiDHsFmltvmC3R2zcu5LdbnHm2N9SQxWafJo4iYwwIhbTtCiXF1S/AI3bwqfWnnNeEAepJuRK6VOi4vlZnGmKK+4QPq6JuVmcZ86KBXI+2R6wtoNz4iS+Ik7txYFv0lCFNj45TuJguqL/ZeMxa/eaHhonZ07/C8H1wonE26EFPhKfSK4H9ia+Dh06dOjw/8G/sXcmUir28IcAAAAASUVORK5CYII="


@pytest.fixture
def false_example_image_string():
    # Properly padded base64 image string
    return "falss-base64"


@pytest.fixture
def expected_result():
    return "(715) 305-5091\n"
