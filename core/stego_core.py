import cv2
import numpy as np

class Steganography:
    """
    Implements LSB (Least Significant Bit) Steganography logic.
    """
    
    def __init__(self):
        self.delimiter = "#####"

    def __msg_to_bin(self, msg):
        """Convert string to binary format."""
        if type(msg) == str:
            return ''.join([format(ord(i), "08b") for i in msg])
        elif type(msg) == bytes or type(msg) == np.ndarray:
            return [format(i, "08b") for i in msg]
        elif type(msg) == int or type(msg) == np.uint8:
            return format(msg, "08b")
        else:
            raise TypeError("Input type not supported")

    def __bin_to_msg(self, binary_str):
        """Convert binary string to ASCII string."""
        all_bytes = [binary_str[i: i+8] for i in range(0, len(binary_str), 8)]
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == self.delimiter:
                break
        return decoded_data[:-5]  # Remove delimiter

    def encode(self, image_path, data, output_path):
        """
        Hides data into image_path and saves to output_path.
        """
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at {image_path}")

        # Maximum bytes to encode
        n_bytes = image.shape[0] * image.shape[1] * 3 // 8
        if len(data) > n_bytes:
            raise ValueError(f"Insufficient bytes, need bigger image or less data. Max bytes: {n_bytes}")

        print(f"[*] Encoding data...")
        
        # Add delimiter to data
        data += self.delimiter
        
        data_index = 0
        binary_secret_msg = self.__msg_to_bin(data)
        data_len = len(binary_secret_msg)
        
        encoded_image = image.copy()
        
        # Flatten the image to iterate over pixels easily
        # image is (Height, Width, Channel)
        # We can iterate over rows, or just flatten it.
        # Let's iterate generally to keep it readable.
        
        # Simple iterator based approach
        rows, cols, channels = image.shape
        
        break_loop = False
        for row in range(rows):
            for col in range(cols):
                pixel = image[row, col]
                
                # pixel is [B, G, R] in OpenCV
                for c in range(channels): # 0, 1, 2
                    if data_index < data_len:
                        # Modify the LSB (Least Significant Bit)
                        # pixel[c] is an int (0-255). 
                        # binary_secret_msg[data_index] is '0' or '1'
                        
                        # Clear LSB: valid_bit = pixel[c] & ~1 (or pixel[c] & 254)
                        # Set LSB: new_val = valid_bit | int(bit)
                        
                        pixel[c] = int(format(pixel[c], '08b')[:-1] + binary_secret_msg[data_index], 2)
                        data_index += 1
                    else:
                        break_loop = True
                        break
                
                encoded_image[row, col] = pixel
                
                if break_loop:
                    break
            if break_loop:
                break
                
        cv2.imwrite(output_path, encoded_image)
        print(f"[*] Encoded image saved to {output_path}")

    def decode(self, image_path):
        """
        Decodes data from the image_path.
        """
        print(f"[*] Decoding data from {image_path}...")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found at {image_path}")
            
        binary_data = ""
        
        rows, cols, channels = image.shape
        
        for row in range(rows):
            for col in range(cols):
                pixel = image[row, col]
                for c in range(channels):
                    binary_data += format(pixel[c], '08b')[-1]
                    
        # Convert binary data to text
        # We process all bits? That might be huge.
        # Optimization: We check for delimiter on the fly or process in chunks.
        # But for basics, let's just grab enough to find delimiter.
        
        # Actually our __bin_to_msg handles the delimiter check loop, 
        # but it expects a full binary string.
        # For large images, passing a massive string is inefficient.
        # Let's write a smarter loop here or inside __bin_to_msg.
        
        # Let's update strategy: Reconstruct bytes on the fly
        all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data.endswith(self.delimiter):
                return decoded_data[:-len(self.delimiter)]
                
        return "No hidden message found or delimiter missing."

