import base64
from PIL import Image
from io import BytesIO


# Function to encode image into Base64
def encode_image_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to byte array using BytesIO
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # Save as PNG or other formats (e.g., JPG)
        img_byte_array = buffered.getvalue()

    # Encode the byte array to base64
    base64_string = base64.b64encode(img_byte_array).decode('utf-8')
    return base64_string


# Function to decode Base64 and save the image
def decode_base64_and_save(encoded_str, output_image_path):
    # Decode the Base64 string into bytes
    image_data = base64.b64decode(encoded_str)

    # Write the decoded data to a new image file
    with open(output_image_path, 'wb') as image_file:
        image_file.write(image_data)

    print(f"Image has been saved to {output_image_path}")


def encode_video_to_base64(video_file_path):
    """
    Encodes a video file to a Base64 string.
    :param video_file_path: Path to the video file.
    :return: Base64 encoded string.
    """
    with open(video_file_path, 'rb') as video_file:
        # Read the video file as binary
        video_bytes = video_file.read()

        # Encode binary data to Base64
        base64_encoded = base64.b64encode(video_bytes).decode('utf-8')

    return base64_encoded


