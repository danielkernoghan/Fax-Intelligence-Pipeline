import os
import shutil
import pytesseract
from pdf2image import convert_from_path

def rdnf_extract_lines(text):
    """
    Extracts lines from text that contain specific keywords related to detection of RDNF form.

    Parameters:
        text (str): The input text from which lines are to be extracted.

    Returns:
        list of str: Lines containing keywords/phrases.
    """
    import re
    pattern = re.compile(r'.*(Reportable Diseases|Notification Form|Reportable Diseases Notification Form|(Reportable Diseases) Notification Form).*', re.IGNORECASE)
    lines = [line.strip() for line in text.split('\n') if pattern.search(line)]
    return lines

def process_rdnf_check(pdf_path, poppler_path, output_folder, rdnf_path):
    """
    Checks if any of the texts indicate that the PDF is an RDNF form.

    Parameters:
    texts (list): A list of text strings extracted from the PDF.

    Returns:
    True: If an RDNF form is detected, the PDF is copied to the RDNF path and the script exits.
    False: Otherwise
    """
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    texts = []
    for i, image in enumerate(images):
        # Save the image as a temporary file
        image_path = os.path.join(output_folder, f'page_{i+1}.png')
        image.save(image_path, 'PNG')
        
        # Detect and correct image orientation
        for angle in [0, 90, 180, 270]:
            rotated_image = image.rotate(angle, expand=True)
            text = pytesseract.image_to_string(rotated_image)
            if 'Reportable Diseases Notification Form' in text:
                break
        texts.append(text)

    for text in texts:
        if rdnf_extract_lines(text):
            os.makedirs(rdnf_path, exist_ok=True)
            shutil.copy(pdf_path, rdnf_path)
            print(f"RDNF form detected and moved: {os.path.basename(pdf_path)}")
            return True

    return False
