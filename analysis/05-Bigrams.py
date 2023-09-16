import pickle
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Function to load data from a pickle file
def load_data_from_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# Basic tokenization method using a predefined set of stop words
def basic_tokenize_without_nltk(text):
    # Splitting by whitespace and punctuation
    tokens = [word for word in text.split() if word.isalpha()]
    # Converting to lowercase
    tokens = [word.lower() for word in tokens]
    # Removing stopwords
    tokens = [word for word in tokens if word not in stop_words_set]
    return tokens

# Function to extract bigrams from tokens
def extract_bigrams(tokens):
    return list(zip(tokens[:-1], tokens[1:]))

# Predefined set of common English stop words
stop_words_set = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
    'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}

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

# Extracting titles and tokenizing them using the basic tokenize method
filtered_iclr_table['tokens'] = filtered_iclr_table['title'].apply(basic_tokenize_without_nltk)

# Extracting bigrams for each title
filtered_iclr_table['bigrams'] = filtered_iclr_table['tokens'].apply(extract_bigrams)

# Aggregating bigrams for all years
all_bigrams = filtered_iclr_table['bigrams'].sum()
all_bigrams_frequency = Counter(all_bigrams)

# Extracting top 20 bigrams across all years
top_bigrams_all_years = all_bigrams_frequency.most_common(20)

# Visualizing the top 20 bigrams
bigrams, frequencies = zip(*top_bigrams_all_years)
bigrams_str = [" ".join(bigram) for bigram in bigrams]

plt.figure(figsize=(15, 10))
plt.barh(bigrams_str, frequencies, color='skyblue')
plt.xlabel('Frequency')
plt.ylabel('Bigrams')
plt.title('Top 20 Bigrams from ICLR Papers (2020-2023)')
plt.gca().invert_yaxis()  # To display the bigram with the highest frequency at the top
plt.tight_layout()
plt.savefig("bigrams_iclr.png", dpi=300, bbox_inches='tight')
plt.show()
