import sys
import os
import cv2
import numpy as np
from core.stego_core import Steganography

def create_sample_image(path):
    """Creates a simple sample image if one doesn't exist."""
    print(f"Creating sample image at {path}")
    # Create a 100x100 RGB image (blue)
    img = np.zeros((100, 100, 3), np.uint8)
    img[:] = (255, 0, 0)
    cv2.imwrite(path, img)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py hide <image_path> <message> <output_path>")
        print("  python main.py reveal <image_path>")
        print("  python main.py test")
        return

    command = sys.argv[1]
    stego = Steganography()
    
    try:
        if command == "hide":
            if len(sys.argv) < 5:
                print("Error: Missing arguments for hide.")
                return
            img_path = sys.argv[2]
            msg = sys.argv[3]
            out_path = sys.argv[4]
            stego.encode(img_path, msg, out_path)
            
        elif command == "reveal":
            if len(sys.argv) < 3:
                print("Error: Missing arguments for reveal.")
                return
            img_path = sys.argv[2]
            result = stego.decode(img_path)
            print(f"Hidden Message: {result}")

        elif command == "test":
            # Self-test
            sample_in = "test_input.png"
            sample_out = "test_output.png"
            secret = "This is a secret message from AntiGravity!"
            
            if not os.path.exists(sample_in):
                create_sample_image(sample_in)
                
            print(f"--- Running Test ---")
            stego.encode(sample_in, secret, sample_out)
            
            decoded = stego.decode(sample_out)
            print(f"Decoded: {decoded}")
            
            if decoded == secret:
                print("SUCCESS: Message matches!")
            else:
                print("FAILURE: Message mismatch.")
                
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
