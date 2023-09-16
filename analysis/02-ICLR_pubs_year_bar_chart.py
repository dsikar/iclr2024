import pickle
import pandas as pd
import matplotlib.pyplot as plt

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

# Group the filtered data by 'publication_year' and count the number of papers for each year
papers_per_year_iclr = filtered_iclr_table.groupby('publication_year').size()

# Plot the number of ICLR publications per year
papers_per_year_iclr_plot = papers_per_year_iclr.plot(kind='bar', figsize=(10, 6), color='skyblue', edgecolor='black')
papers_per_year_iclr_plot.set_title('Number of ICLR Publications (2020-2023)')
papers_per_year_iclr_plot.set_xlabel('Year')
papers_per_year_iclr_plot.set_ylabel('Number of Papers')
plt.tight_layout()
plt.show()

# save plot to file
papers_per_year_iclr_plot.figure.savefig('iclr_publications_per_year.png')

