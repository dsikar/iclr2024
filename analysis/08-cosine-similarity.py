import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to load data from a pickle file
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# Load data
filename = "/home/daniel/git/iclr2024/saved_data/semantic_data_2023-09-15_18-25-14_210_files.pkl" 
data_from_pickle = load_data_from_pickle(filename)
master_list_data = data_from_pickle['master_list']
papers_list_data = data_from_pickle['papers_list']

# Extracting abstracts from papers_list
paper_abstracts_from_papers_list = [entry['abstract'] for entry in papers_list_data if entry['abstract']]

# Transforming abstracts to TF-IDF vectors
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(paper_abstracts_from_papers_list)

# Computing the cosine similarity matrix
cosine_sim_matrix = cosine_similarity(tfidf_matrix)
np.fill_diagonal(cosine_sim_matrix, -1)  # setting diagonal to -1 to exclude self-matches

# Getting the indices of the top 20 most similar paper pairs
top_20_similarities_indices = np.dstack(np.unravel_index(np.argsort(cosine_sim_matrix.ravel())[-20:], cosine_sim_matrix.shape))[0]

# Extracting the corresponding similarity scores and sorting them
sorted_indices = np.argsort([cosine_sim_matrix[i, j] for i, j in top_20_similarities_indices])[::-1]
top_20_similarities_indices = top_20_similarities_indices[sorted_indices]
top_20_similarities_scores = [cosine_sim_matrix[i, j] for i, j in top_20_similarities_indices]

# Extracting the paperIDs corresponding to the indices
top_20_paperID_pairs = [(papers_list_data[i]['paperID'], papers_list_data[j]['paperID']) for i, j in top_20_similarities_indices]

top_20_paperID_pairs, top_20_similarities_scores


# Extracting unique papers from top pairs for the second table
unique_papers_from_top_pairs = list(set([paper for pair in top_20_paperID_pairs for paper in pair]))

# Filter out papers that have abstracts and are in papers_list_data
papers_with_abstracts = [entry for entry in papers_list_data if entry['abstract']]

# Mapping indices from master_list_data to their corresponding indices in papers_with_abstracts
index_mapping = {entry['paperID']: idx for idx, entry in enumerate(papers_with_abstracts)}

# Filtering pairs where both paperIDs are in papers_with_abstracts
filtered_unique_pairs = [(paper1, paper2) for paper1, paper2 in unique_top_20_pairs if paper1 in index_mapping and paper2 in index_mapping]

# Sorting the filtered unique pairs by cosine similarity score in descending order
sorted_filtered_pairs = sorted(filtered_unique_pairs, key=lambda pair: cosine_similarity_matrix[index_mapping[pair[0]], index_mapping[pair[1]]], reverse=True)

# Generating LaTeX table for sorted unique top 20 similar paper pairs
latex_table_sorted_pairs = "\\begin{table}[h!]\n"
latex_table_sorted_pairs += "\\centering\n"
latex_table_sorted_pairs += "\\begin{tabular}{|c|c|c|c|}\n"
latex_table_sorted_pairs += "\\hline\n"
latex_table_sorted_pairs += "Index & Paper 1 (Index in master\\_list) & Paper 2 (Index in master\\_list) & Cosine Similarity Score\\\\\n"
latex_table_sorted_pairs += "\\hline\n"

for idx, (paper1, paper2) in enumerate(sorted_filtered_pairs, 1):
    paper1_idx_in_master = next(i for i, entry in enumerate(master_list_data) if entry['paperID'] == paper1)
    paper2_idx_in_master = next(i for i, entry in enumerate(master_list_data) if entry['paperID'] == paper2)
    score = cosine_similarity_matrix[index_mapping[paper1], index_mapping[paper2]]
    latex_table_sorted_pairs += f"{idx} & {paper1_idx_in_master} & {paper2_idx_in_master} & {score:.3f}\\\\\n"
latex_table_sorted_pairs += "\\hline\n"
latex_table_sorted_pairs += "\\end{tabular}\n"
latex_table_sorted_pairs += "\\caption{Top most similar unique paper pairs based on abstract cosine similarity (sorted in descending order)}\n"
latex_table_sorted_pairs += "\\end{table}\n"

latex_table_sorted_pairs


# Generating LaTeX table for unique papers in top pairs with correct source for title
latex_table_papers = "\\begin{table}[h!]\n"
latex_table_papers += "\\centering\n"
latex_table_papers += "\\begin{tabular}{|c|c|c|}\n"
latex_table_papers += "\\hline\n"
latex_table_papers += "Index & Paper Index in master\\_list & Title\\\\\n"
latex_table_papers += "\\hline\n"
for idx, paperID in enumerate(unique_papers_from_top_pairs, 1):
    paper_idx = next(i for i, entry in enumerate(master_list_data) if entry['paperID'] == paperID)
    title = next(entry['title'] for entry in master_list_data if entry['paperID'] == paperID)
    latex_table_papers += f"{idx} & {paper_idx} & {title}\\\\\n"
latex_table_papers += "\\hline\n"
latex_table_papers += "\\end{tabular}\n"
latex_table_papers += "\\caption{Papers appearing in the top similar pairs table}\n"
latex_table_papers += "\\end{table}\n"

latex_table_pairs, latex_table_papers
