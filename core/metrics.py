import cv2
import numpy as np
import math

class StegoMetrics:
    """
    Calculates image quality metrics to measure distortion.
    """
    
    @staticmethod
    def calculate_mse(image1_path, image2_path):
        """
        Calculates Mean Squared Error between two images.
        """
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        if img1 is None or img2 is None:
            raise ValueError("One or both images could not be loaded")
            
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same dimensions")
            
        # MSE = Sum of squared difference / number of pixels
        # We can use numpy for fast calculation
        
        # Convert to float to avoid overflow during subtraction (uint8 wraps around)
        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        
        diff = img1 - img2
        sq_diff = diff ** 2
        
        mse = np.mean(sq_diff)
        return mse

    @staticmethod
    def calculate_psnr(image1_path, image2_path):
        """
        Calculates Peak Signal-to-Noise Ratio (dB).
        """
        mse = StegoMetrics.calculate_mse(image1_path, image2_path)
        
        if mse == 0:
            return float('inf') # Identical images
            
        # Max possible pixel value is 255
        max_pixel = 255.0
        
        psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
        return psnr

    @staticmethod
    def compare_histograms(image1_path, image2_path):
        """
        Compares histograms of two images.
        Returns a dictionary with correlation values for each channel (B, G, R).
        1.0 means perfect fit.
        """
        img1 = cv2.imread(image1_path)
        img2 = cv2.imread(image2_path)
        
        results = {}
        colors = ('b', 'g', 'r')
        
        for i, col in enumerate(colors):
            hist1 = cv2.calcHist([img1], [i], None, [256], [0, 256])
            hist2 = cv2.calcHist([img2], [i], None, [256], [0, 256])
            
            # Normalize histograms
            cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            
            # Compare using Correlation method
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            results[col] = similarity
            
        return results
