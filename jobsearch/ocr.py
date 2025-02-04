import pdfplumber
import os
import re
import csv

def extract_text(pdf_file_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"An error occurred while processing {pdf_file_path}: {e}")
        return None
    return text

def parse_sections(pdf_text):
    """Parses specific sections (Education, Skills, Work Experience, Projects) from PDF text."""
    sections = {
        "Education": "",
        "Skills": "",
        "Work Experience": "",
        "Projects": ""
    }
    
    # Define patterns for the headings
    patterns = {
        "Education": r"(?i)(Education|EDUCATION)",
        "Skills": r"(?i)(Skills|SKILLS)",
        "Work Experience": r"(?i)(Work Experience|WORK EXPERIENCE|Experience|EXPERIENCE)",
        "Projects": r"(?i)(Projects|PROJECTS)"
    }
    
    # Find positions of each section
    section_positions = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, pdf_text)
        if match:
            section_positions[key] = match.start()
    
    # Sort sections by their starting positions
    sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
    
    # Extract content for each section
    for i, (section, start_pos) in enumerate(sorted_sections):
        # Determine the end position as the start of the next section or the end of the text
        end_pos = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(pdf_text)
        section_content = pdf_text[start_pos:end_pos].strip()
        
        # Remove the heading itself from the extracted content
        heading_match = re.match(patterns[section], section_content, re.IGNORECASE)
        if heading_match:
            section_content = section_content[heading_match.end():].strip()
        
        # Assign the cleaned content to the section
        sections[section] = section_content
    
    return sections

def process_pdfs_in_folder_to_csv(folder_path, output_csv_file):
    """Processes all PDFs in a folder and stores extracted data in a CSV file."""
    # Open the CSV file for writing
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['filename', 'section', 'content']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        
        # Iterate through all PDF files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".pdf"):
                pdf_file_path = os.path.join(folder_path, filename)
                print(f"Processing {filename}...")
                
                pdf_text = extract_text(pdf_file_path)
                if pdf_text:
                    pdf_data = parse_sections(pdf_text)
                    
                    # Write each section's content to the CSV
                    for section_name, section_content in pdf_data.items():
                        if section_content:  # Only add non-empty sections
                            writer.writerow({
                                'filename': filename,
                                'section': section_name,
                                'content': section_content
                            })
    
    print(f"All PDFs processed and data stored in {output_csv_file}.")

# Replace 'pdf_folder_path' with the path to your folder containing PDFs
pdf_folder_path = "/Users/princypatel/Desktop/ML Projects/AI-Agents/jobsearch/resumes"

# Replace with the desired path for the CSV output file
output_csv_file = "/Users/princypatel/Desktop/ML Projects/AI-Agents/jobsearch/resume_data.csv"

# Process all PDFs in the folder and store the sections in CSV
process_pdfs_in_folder_to_csv(pdf_folder_path, output_csv_file)
