import pickle
import os
from PyPDF2 import PdfFileReader

def load_data_from_pickle(filename, filepath="."):
    """
    Load papers_list from a pickle file.
    """
    # Construct the full path for reading the pickle file
    load_path = os.path.join(filepath, filename)

    # Ensure the file exists
    if not os.path.exists(load_path):
        print(f"File {load_path} not found!")
        return None

    # Deserialize and load the data
    with open(load_path, 'rb') as file:
        data = pickle.load(file)
        papers_list = data.get("papers_list", [])

    return papers_list

def convert_pdf_to_text(pdf_path):
    """
    Convert a PDF file to text.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfFileReader(file)
        text = ""
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extractText()
    return text

def generate_training_prompts(papers_list, directory_path="."):
    """
    Generate training prompts for the language model based on the text extracted from PDFs.
    """
    prompts = []
    for paper in papers_list:
        arxiv_id = paper.get("arxivId")
        if arxiv_id:
            pdf_path = os.path.join(directory_path, f"{arxiv_id}.pdf")
            if os.path.exists(pdf_path):
                text = convert_pdf_to_text(pdf_path)
                prompts.append(text)  # This can be further refined based on the desired format for training
    return prompts

def submit_to_cloud_provider(prompts):
    """
    Submit the generated prompts to the cloud provider for training the language model.
    """
    # Implementation would depend on the specific cloud provider and their API
    pass

def main():
    """
    Main function to orchestrate the PDF-to-text conversion and training prompt generation.
    """
    # Load data from pickle file
    papers_list = load_data_from_pickle("semantic_data.pkl", "./saved_data")

    # Generate training prompts
    prompts = generate_training_prompts(papers_list, "./saved_data")

    # Submit prompts to cloud provider for training
    submit_to_cloud_provider(prompts)

if __name__ == "__main__":
    main()
