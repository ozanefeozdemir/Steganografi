from core.stego_core import Steganography
from core.metrics import StegoMetrics
import os

def run_validation():
    print("=== Steganography Validation Suite ===")
    
    stego = Steganography()
    metrics = StegoMetrics()
    
    # 1. Setup paths
    input_img = "test_input.png"
    output_img = "test_output.png"
    
    # Ensure input image exists
    if not os.path.exists(input_img):
        print("Creating sample image...")
        import numpy as np
        import cv2
        img = np.zeros((100, 100, 3), np.uint8)
        img[:] = (255, 0, 0)
        cv2.imwrite(input_img, img)

    # 2. Test Cases
    messages = [
        "A", 
        "Hello World", 
        "This is a longer message to test how the noise affects the image quality significantly more than a short one."
    ]
    
    print(f"\n{'Message Length':<15} | {'MSE':<10} | {'PSNR (dB)':<10} | {'Hist Corr (Avg)':<15}")
    print("-" * 60)
    
    for msg in messages:
        # Encode
        stego.encode(input_img, msg, output_img)
        
        # Calculate Metrics
        mse = metrics.calculate_mse(input_img, output_img)
        psnr = metrics.calculate_psnr(input_img, output_img)
        hist_sim = metrics.compare_histograms(input_img, output_img)
        avg_sim = sum(hist_sim.values()) / 3
        
        print(f"{len(msg):<15} | {mse:<10.5f} | {psnr:<10.2f} | {avg_sim:<15.4f}")
        
    print("\n[+] Validation Complete.")
    
if __name__ == "__main__":
    run_validation()
