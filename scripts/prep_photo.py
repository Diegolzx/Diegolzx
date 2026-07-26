import sys
from PIL import Image
import numpy as np
import cv2
from rembg import remove

def prep_photo(input_path, output_path):
    print(f"Processing {input_path}...")
    # Read the image
    # Read the image and remove background
    print("Removing background (PIL)...")
    input_image = Image.open(input_path)
    subject = remove(input_image)

    
    # Convert to numpy array for OpenCV
    subject_np = np.array(subject)
    
    # Extract alpha channel
    if subject_np.shape[2] == 4:
        b, g, r, a = cv2.split(subject_np)
        bgr = cv2.merge([b, g, r])
    else:
        bgr = subject_np
        a = np.ones(bgr.shape[:2], dtype=np.uint8) * 255
    
    # Convert to LAB for CLAHE
    lab = cv2.cvtColor(bgr, cv2.COLOR_RGB2LAB)
    l, a_channel, b_channel = cv2.split(lab)
    
    # Apply CLAHE to L channel
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    
    # Merge back and convert to RGB
    limg = cv2.merge((cl, a_channel, b_channel))
    enhanced_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)
    
    # Composite onto white background
    print("Compositing onto white background...")
    white_bg = np.ones_like(enhanced_bgr) * 255
    alpha_factor = a.astype(float) / 255.0
    alpha_factor = np.stack([alpha_factor]*3, axis=2)
    
    composited = (enhanced_bgr * alpha_factor + white_bg * (1 - alpha_factor)).astype(np.uint8)
    
    # Convert to grayscale for final output
    gray = cv2.cvtColor(composited, cv2.COLOR_RGB2GRAY)
    
    # Save output
    cv2.imwrite(output_path, gray)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_photo.py <input_image>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "source-prepped.png"
    prep_photo(input_file, output_file)
