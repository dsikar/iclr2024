import pickle
import pandas as pd

# Function to load data from a pickle file
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# Load data from the pickle file
filename = "/home/daniel/git/iclr2024/saved_data/semantic_data_2023-09-15_18-25-14_210_files.pkl" 
data_from_pickle = load_data_from_pickle(filename)

# Extracting master_list and papers_list from the loaded data
master_list_data = data_from_pickle['master_list']
papers_list_data = data_from_pickle['papers_list']

# Extracting the paperIDs from papers_list
paper_ids_iclr = [paper['paperID'] for paper in papers_list_data]

# Filtering the master_list_data to only include entries with paperIDs that are present in papers_list
filtered_iclr_publications = [entry for entry in master_list_data if entry['paperID'] in paper_ids_iclr]

# Convert the filtered data into a table format for easier analysis
filtered_iclr_table = pd.DataFrame(filtered_iclr_publications)

# Sorting the table by 'publication_year' and 'title' in ascending order
sorted_table = filtered_iclr_table.sort_values(by=['publication_year', 'title']).reset_index(drop=True)
sorted_table = sorted_table[['title', 'publication_year']]
sorted_table['index'] = range(1, len(sorted_table) + 1)

# Rearranging the columns to have 'index', 'title', and 'publication_year'
final_table = sorted_table[['index', 'title', 'publication_year']]
print(final_table)

# If you wish to save the table to a CSV file, you can use the following line:
final_table.to_csv("iclr_papers_table.csv", index=False)
