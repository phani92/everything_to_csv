# Author: Phani!
# Description: This script converts xlsx file to csv file and pdf file to csv file.
# Usage: python xlsxTocsv.py <input_file> <output_file>

import sys
import pandas as pd
import PyPDF2

def xlsx_to_csv(input_file, output_file):
    # Read the xlsx file
    df = pd.read_excel(input_file)
    # Convert the xlsx file to csv file
    df.to_csv(output_file, index=False)
    print('File converted successfully.')

def pdf_to_csv(input_file, output_file):
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    # Initialize an empty list to store text lines
    text_data = []
    # Iterate through each page in the PDF
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        # Split text into lines and add to the list
        lines = text.split('\n')
        text_data.extend(lines)
    # Convert list of text lines into a DataFrame
    df = pd.DataFrame(text_data, columns=['Text'])
    # Write DataFrame to CSV
    df.to_csv(output_file, index=False)
    print('File converted successfully.')

if __name__ == '__main__':
    # Sys args for user inputs
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # Validate user inputs
    if not input_file.endswith('.xlsx') and not input_file.endswith('.pdf'):
        print('Input file should be in xlsx or pdf format')
        exit()
    if not output_file.endswith('.csv'):
        print('Output file should be in csv format')
        exit()
    # Check if the input file exists
    try:
        with open(input_file, 'rb') as file:
            # Give option to user to convert xlsx to csv or pdf to csv
            print('1. Convert xlsx to csv')
            print('2. Convert pdf to csv')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                xlsx_to_csv(input_file, output_file)
            elif choice == 2:
                pdf_to_csv(input_file, output_file)
            else:
                print('Invalid choice')
                exit()
    except FileNotFoundError:
        print('File not found')
