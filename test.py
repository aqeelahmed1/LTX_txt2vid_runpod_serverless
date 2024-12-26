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


# Example usage:
# Encode the image to Base64
input_image = 'test.jpg'  # Replace with your input image path
encoded_string = encode_image_to_base64(input_image)

# Save the Base64 string to a text file (optional)


# Now, decode the Base64 string and save it back to an image
decoded_image_path = 'decoded_image.png'  # Path where the image will be saved
decode_base64_and_save(encoded_string, decoded_image_path)
