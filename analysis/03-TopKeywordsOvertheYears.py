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

# Grouping the tokens by year
grouped_tokens = filtered_iclr_table.groupby('publication_year')['tokens'].sum()

# Calculating word frequencies for each year
word_frequencies_per_year = grouped_tokens.apply(Counter)

# Extracting top keywords for each year
top_keywords_per_year = word_frequencies_per_year.apply(lambda x: x.most_common(5))

# Visualizing the Top Keywords Over the Years
top_keywords = set()
for year, keywords in top_keywords_per_year.items():
    for keyword, _ in keywords:
        top_keywords.add(keyword)

# Preparing data for visualization
keywords_over_years = {}
for keyword in top_keywords:
    yearly_counts = []
    for year, keywords in word_frequencies_per_year.items():
        yearly_counts.append(keywords[keyword])
    keywords_over_years[keyword] = yearly_counts

# Plotting the trends of top keywords over the years at ICLR
plt.figure(figsize=(15, 10))
for keyword, yearly_counts in keywords_over_years.items():
    plt.plot(word_frequencies_per_year.keys(), yearly_counts, label=keyword, marker='o')

plt.title('Trends of Top Keywords Over the Years at ICLR')
plt.xlabel('Year')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# save plot to file
plt.savefig("TopKeywordsOvertheYears_iclr.png", dpi=300, bbox_inches='tight')

