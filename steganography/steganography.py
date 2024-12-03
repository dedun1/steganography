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
def decode_message(image_path):
    """Decodes a secret message from a BMP image."""
    binary_message = ''.join(str(byte & 1) for byte in read_and_prepare_image(image_path)[54:])  # Extract the LSBs from pixel data after the BMP header
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))  # Convert binary data back to characters
    if "#END#" in decoded_message:  # Check if the decoded message contains the #END# delimiter
        print(f"Decrypted Message: {decoded_message.split('#END#')[0]}")  # Print the message up to the delimiter 
    else:
        raise ValueError("No valid message found in the image.")  # Raise an error if the delimiter is not found


if __name__ == "__main__":
    print("Welcome to the Steganography Program!")  # Print the welcome message
    choice = input("1. Encode\n2. Decode\n3. Exit\nEnter your choice (1/2/3): ").strip()  # Prompt the user to select an option
   
    try:
        if choice == "1":  # If the user selects encoding
            input_file = input("Enter BMP file to encode into: ").strip()  # Prompt for the input BMP file
            output_file = input("Enter output BMP file name: ").strip()  # Prompt for the output BMP file name
            secret_message = input("Enter your secret message: ").strip()  # Prompt for the secret message
            encode_message(input_file, secret_message, output_file)  # Call the encode function with the user inputs
        elif choice == "2":  # If the user selects decoding
            input_file = input("Enter BMP file to decode from: ").strip()  # Prompt for the input BMP file
            decode_message(input_file)  # Call the decode function with the user input
        elif choice == "3":  # If the user selects exit
            print("Exiting the program. Goodbye!")  # Print a goodbye message
        else:  # If the user enters an invalid choice
            print("Invalid choice! Please select 1, 2, or 3.")  # Inform the user of an invalid input
    except FileNotFoundError:  # Handle the case where the specified file is not found
        print("Error: The specified BMP file was not found.")  # Print an error message
    except ValueError as ve:  # Handle value errors like a message that's too long
        print(f"Error: {ve}")  # Print the specific error message
    except Exception as e:  # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")  # Print a general error message