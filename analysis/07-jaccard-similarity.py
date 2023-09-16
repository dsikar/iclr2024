import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import numpy as np

# Function to load data from a pickle file
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def jaccard_similarity(set1, set2):
    """Compute the Jaccard Similarity between two sets."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0  # Avoid division by zero
    return intersection / union

# Load data from the pickle file
filename = "/home/daniel/git/iclr2024/saved_data/semantic_data_2023-09-15_18-25-14_210_files.pkl"  
data_from_pickle = load_data_from_pickle(filename)

# Extracting master_list and papers_list from the loaded data
master_list_data = data_from_pickle['master_list']
papers_list_data = data_from_pickle['papers_list']

# Extracting reference sets for each paperID in papers_list
paper_references = {paper['paperID']: set(paper['references']) for paper in papers_list_data}

# Assuming you have the paper_references dictionary loaded
all_paper_ids = list(paper_references.keys())
jaccard_matrix = np.zeros((len(all_paper_ids), len(all_paper_ids)))

for i, paper_id1 in enumerate(all_paper_ids):
    for j, paper_id2 in enumerate(all_paper_ids):
        if i <= j:  # To avoid repeated calculations
            similarity = jaccard_similarity(paper_references[paper_id1], paper_references[paper_id2])
            jaccard_matrix[i, j] = similarity
            jaccard_matrix[j, i] = similarity  # Due to symmetry

# Plotting the heatmap
sns.set(rc={"axes.facecolor":"white", "axes.grid":False})

plt.figure(figsize=(12, 10))
ax = sns.heatmap(jaccard_matrix, cmap="YlGnBu", xticklabels=100, yticklabels=100, cbar_kws={'label': 'Jaccard Similarity'})
ax.set_title('Pairwise Jaccard Similarities for Paper References')
ax.set_xlabel('Paper Index')
ax.set_ylabel('Paper Index')
plt.tight_layout()
plt.savefig("jaccard_similarity_heatmap.png")
plt.show()

# Adjusting the mapping creation for paperID to index based on the order in master_list_data
paper_id_to_index = {entry['paperID']: idx for idx, entry in enumerate(master_list_data)}

# Extracting the top 20 most similar paper pairs again
jaccard_indices = np.triu_indices_from(jaccard_matrix, k=1)  # Upper triangular indices without diagonal
jaccard_values = jaccard_matrix[jaccard_indices]
sorted_indices = np.argsort(jaccard_values)[::-1][:20]  # Indices for the top 20 values

top_20_paper_pairs = [(all_paper_ids[i], all_paper_ids[j], jaccard_values[idx]) for idx, (i, j) in enumerate(zip(*jaccard_indices)) if idx in sorted_indices]

# Replacing the paperIDs in top_20_paper_pairs with their corresponding indices
top_20_index_pairs = [(paper_id_to_index[paper_id1], paper_id_to_index[paper_id2], similarity) for paper_id1, paper_id2, similarity in top_20_paper_pairs]

# Sorting the pairs by descending order of Jaccard Similarity
top_20_index_pairs_sorted = sorted(top_20_index_pairs, key=lambda x: x[2], reverse=True)

# Generating the LaTeX table for the top 20 most similar paper pairs using indices
latex_table_indexed_1 = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|c|c|c|c|}\n\\hline\n"
latex_table_indexed_1 += "Index & Paper Index 1 & Paper Index 2 & Jaccard Similarity \\\\\n\\hline\n"
for idx, (index1, index2, similarity) in enumerate(top_20_index_pairs_sorted, start=1):
    latex_table_indexed_1 += f"{idx} & {index1} & {index2} & {similarity:.4f} \\\\\n"
latex_table_indexed_1 += "\\hline\n\\end{tabular}\n\\caption{Top 20 most similar papers based on Jaccard Similarity (using indices)}\n\\end{table}"

latex_table_indexed_1

# save table to file
with open("jaccard_similarity_table_indexed_1.txt", "w") as file:
    file.write(latex_table_indexed_1)

# Extracting the unique indices from the top 20 most similar paper pairs
unique_indices = list(set([index for pair in top_20_index_pairs_sorted for index in pair[:2]]))

# Extracting the titles for the unique indices
index_title_map = {index: master_list_data[index]['title'] for index in unique_indices}

# Generating the LaTeX table for the unique indices and their titles
latex_table_indexed_2 = "\\begin{table}[h]\n\\centering\n\\begin{tabular}{|c|c|l|}\n\\hline\n"
latex_table_indexed_2 += "Index & Paper Index & Title \\\\\n\\hline\n"
for idx, (index, title) in enumerate(sorted(index_title_map.items(), key=lambda x: x[1]), start=1):
    # Shortening long titles for presentation
    short_title = (title[:60] + '...') if len(title) > 60 else title
    latex_table_indexed_2 += f"{idx} & {index} & {short_title} \\\\\n"
latex_table_indexed_2 += "\\hline\n\\end{tabular}\n\\caption{Titles for papers in the top 20 similarity list (using indices)}\n\\end{table}"

latex_table_indexed_2

# save table to file
with open("jaccard_similarity_table_indexed_2.txt", "w") as file:
    file.write(latex_table_indexed_2)



