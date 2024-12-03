def read_and_prepare_image(image_path):
    """Reads a BMP image and converts it to a bytearray."""
    with open(image_path, 'rb') as file:  # Open the BMP file in binary read mode
        return bytearray(file.read())  # Read the file content and convert it to a bytearray


def prepare_binary_message(message):
    """Converts a message to binary and appends a #END# delimiter."""
    return ''.join(format(ord(char), '08b') for char in message + "#END#")  # Convert each character to binary and concatenate


def encode_message(image_path, message, output_path):
    """Encodes a secret message into a BMP image."""
    image_data = read_and_prepare_image(image_path)  # Read the image data as a bytearray
    binary_message = prepare_binary_message(message)  # Convert the message into binary form with a delimiter
    if len(binary_message) > (len(image_data) - 54) * 8:  # Check if the binary message fits in the available pixel data
        raise ValueError("Message too long for the selected image.")  # Raise an error if the message is too large


    i = 54  # Start counter after the BMP header
    for bit in binary_message:  # Iterate over each bit of the binary message
        image_data[i] = (image_data[i] & 0xFE) | int(bit)  # Clear the LSB and set it to the current bit of the message
        i += 1  # Increment the counter manually


    with open(output_path, 'wb') as file:  # Open the output file in binary write mode
        file.write(image_data)  # Write the modified bytearray to the file
    print(f"Message successfully saved to: {output_path}")  # Print a success message