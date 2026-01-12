# Visual Steganography Project (LSB Implementation)

## Project Overview
This project implements a steganography tool based on the Least Significant Bit (LSB) algorithm. It allows users to hide text messages within PNG images and retrieve them later without noticeable loss in image quality. The primary goal is to demonstrate "Security through Obscurity" by manipulating the binary data of pixels.

## Features
- **Hide Data**: Encrypts text into the LSB of image pixels.
- **Reveal Data**: Extracts hidden text from steganographic images.
- **Image Quality Analysis**: Includes tools to calculate MSE (Mean Squared Error) and PSNR (Peak Signal-to-Noise Ratio).
- **Dual Interface**: Supports both a Command Line Interface (CLI) and a Graphical User Interface (GUI).
- **Format Support**: Optimized for PNG images to prevent data loss due to compression.

## Installation

1. Clone the repository or download the source code.
2. Initialize a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Graphical User Interface (GUI)
The most convenient way to use the application is through the GUI.
1. Run the application:
   ```bash
   python gui.py
   ```
2. **To Hide a Message**:
   - Go to the "Hide Message" tab.
   - Click "Select Image" to choose a base PNG image.
   - Enter your secret text in the text box.
   - Click "Encrypt & Hide" button and save the new image.
3. **To Reveal a Message**:
   - Go to the "Reveal Message" tab.
   - Select the image containing the hidden message.
   - Click "Decrypt & Reveal". The text will appear in the output box.

### Command Line Interface (CLI)
You can also use the tool via the terminal.

**Hide a Message:**
```bash
python main.py hide <input_image_path> "<secret_message>" <output_image_path>
```
Example:
```bash
python main.py hide original.png "This is a secret" stego.png
```

**Reveal a Message:**
```bash
python main.py reveal <stego_image_path>
```
Example:
```bash
python main.py reveal stego.png
```

**Run Self-Test:**
```bash
python main.py test
```

## Technical Details

### LSB Algorithm
The core logic resides in `core/stego_core.py`. The algorithm works by:
1. Converting the secret message into a binary string.
2. Iterating through the image pixels (Red, Green, Blue channels).
3. Replacing the last bit (LSB) of each channel-byte with a bit from the message.
4. Using a delimiter ("#####") to mark the end of the message.

### Metrics
The project enforces quality control using metrics defined in `core/metrics.py`:
- **MSE**: Measures the average squared difference between the original and modified pixel values. Ideally close to 0.
- **PSNR**: Measures the quality of reconstruction in decibels (dB). Values above 40dB indicate excellent quality invisible to the human eye.

## Project Structure
- `core/`
  - `stego_core.py`: Implementation of the LSB encoding/decoding logic.
  - `metrics.py`: Functions for calculating distortion metrics (MSE, PSNR, Histogram).
- `gui.py`: Tkinter-based graphical interface.
- `main.py`: CLI entry point.
- `validation.py`: Script to run automated validation tests.
- `requirements.txt`: List of Python dependencies.
