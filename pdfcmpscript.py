import os
import shutil
from PyPDF2 import PdfReader, PdfWriter


def compress_pdf(directory_path):
    pdf_files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]
    if len(pdf_files) == 0:
        print(f"No pdfs found in {directory_path}")
        return
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a valid directory")
        return
    for file in pdf_files:
        # Open the PDF file in read-binary mode
        file = open(os.path.join(directory_path, file), 'rb')
        # Create a PDF reader object
        reader = PdfReader(file)
        # Create a PDF writer object
        writer = PdfWriter()
        # Compress the PDF until the size is small enough
        counter = 0
        while counter < 5:
            # Compress the PDF
            for page in reader.pages:
                page.compress_content_streams()
                writer.add_page(page)
            # Write the compressed version to a temporary file
            temp_path = os.path.join(directory_path, file + '.tmp')
            with open(temp_path, 'wb') as temp_file:
                writer.write(temp_file)
            # Close the original file
            file.close()
            # Check the size of the compressed file
            if os.path.getsize(temp_path) <= 25 * 1024 * 1024:
                # The size is small enough, so replace the original file with the compressed version
                shutil.move(temp_path, os.path.join(directory_path, file))
                break
            else:
                # The size is still too large, so try compressing again
                file = open(os.path.join(directory_path, file), 'rb')
                reader = PdfReader(file)
                writer = PdfWriter()
                counter += 1


directory_path = input("Enter the path to the directory containing the PDF files:")
compress_pdf(directory_path)


