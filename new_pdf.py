import os
import pathlib
from pypdf import PdfReader

directory = "cryptography"

for fname in os.listdir(directory):
    file_path = os.path.join(directory, fname)
    
    # Check if it's a PDF file
    if fname.lower().endswith('.pdf'):
        # Open and read the PDF
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        # Save the extracted text as a .txt file
        output_path = pathlib.Path(file_path + ".txt")
        output_path.write_text(text)

