import pickle
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

def load_data_from_pickle(filename, filepath="."):
    """
    Load master_list and papers_list from a pickle file.
    """
    # Construct the full path for reading the pickle file
    load_path = os.path.join(filepath, filename)

    # Ensure the file exists
    if not os.path.exists(load_path):
        print(f"File {load_path} not found!")
        return None, None

    # Deserialize and load the data
    with open(load_path, 'rb') as file:
        data = pickle.load(file)
        master_list = data.get("master_list", [])
        papers_list = data.get("papers_list", [])

    return master_list, papers_list

def compute_similarity_scores(master_list):
    """
    Compute similarity scores between papers based on their abstracts or other relevant data.
    """
    
    # Convert the master list to a numpy array
    master_array = np.array(master_list)
    
    # Compute the cosine similarity matrix
    similarity_matrix = cosine_similarity(master_array)
    
    # Return the similarity matrix
    return similarity_matrix

def visualize_similarity_results(similarity_scores):
    """
    Visualize the similarity results, e.g., using a heatmap or a dendrogram.
    """
    # Create a heatmap of the similarity scores
    fig, ax = plt.subplots()
    im = ax.imshow(similarity_scores, cmap="YlGnBu")
    
    # Add a colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Similarity Score", rotation=-90, va="bottom")
    
    # Set the axis labels
    ax.set_xlabel("Paper Index")
    ax.set_ylabel("Paper Index")
    
    # Set the title
    ax.set_title("Cosine Similarity Matrix")
    
    # Show the plot
    plt.show()

def write_list_to_file(lst, filename):
    # Open the file for writing
    with open(filename, "w") as file:
        # Write each element in the list to a separate line in the file
        for element in lst:
            line = str(element)
            file.write(line + "\n")  

def main():
    """
    Main function to orchestrate the analysis and visualization.
    """
    # Load data from pickle file
    # papers_list ~ {'paperID': 'fd4c076e0229ccd1a992...fd4adcb7ad', 'references': ['9f1b0e4c4 ...
    # master_list ~ {'title': 'Scaling Up Your Kern...gn in CNNs', 'paperID': '9f1b0e4c42a5 ...
    master_list, papers_list = load_data_from_pickle("semantic_data_2023-09-15_18-25-14_210_files.pkl", "./saved_data")
    write_list_to_file(master_list, "master_list.txt")
    write_list_to_file(papers_list, "papers_list.txt")

    # Compute similarity scores
    similarity_scores = compute_similarity_scores(master_list)

    # Visualize the results
    visualize_similarity_results(similarity_scores)

if __name__ == "__main__":
    main()
