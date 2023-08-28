import os
from semantic_scholar import SemanticScholar

def process_paper_title(ss, title):
    """Fetch and store all data related to the given paper title."""
    paperID = ss.get_paper_id_by_title(title)
    if not paperID:
        print(f"Failed to find paperID for title: {title}")
        return

    bibtex, arxiv_id, publication_year, abstract = ss.get_paper_details(paperID)
    references = ss.fetch_and_store_references(paperID)
    ss.add_to_papers_list(paperID, references)

    # Create a directory named based on the publication year and download the ArXiv PDF
    directory_name = "iclr_" + publication_year
    ss.download_arxiv_pdf(arxiv_id, directory_name)

def main():
    # Initialize the SemanticScholar class with debug mode turned on
    ss = SemanticScholar(debug=True)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Build the path to the data file
    file_path = os.path.join(script_dir, '..', 'data', 'ICLR2020-2023_3_Papers.txt')
    
    # Open the file for reading
    with open(file_path, "r") as file:
        # Iterate through each line in the file
        for line in file:
            # Strip leading and trailing whitespace (including newline characters)
            stripped_line = line.strip()
            
            # Check if the line is not blank and doesn't start with '#'
            if stripped_line and not stripped_line.startswith("#"):
                process_paper_title(ss, stripped_line)

    # Save the data to a pickle file after processing all titles
    ss.store_data_as_pickle("semantic_data.pkl", "./saved_data")

if __name__ == "__main__":
    main()
