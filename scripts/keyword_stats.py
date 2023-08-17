import re
import time
from collections import Counter
import string
import matplotlib.pyplot as plt

# Define a list of common stop words
stop_words = set([
    "and", "in", "the", "from", "by", "on", "with", "as", "for", "to",
    "is", "of", "at", "an", "a", "or", "that", "this", "it", "are", "be",
    "was", "were", "will", "have", "has", "had", "not", "but", "if", "which"
])

def extract_titles_from_file(filename):
    """Extract paper titles from a given file."""
    with open(filename, 'r') as file:
        content = file.readlines()

    # Regular expression to extract the title
    pattern = r'<li><a href=".*?">(.*?)</a></li>'
    titles = [re.search(pattern, line).group(1) for line in content if re.search(pattern, line)]
    return titles

def get_word_frequency(titles):
    """Extract and count words from titles excluding stop words."""
    words = []
    for title in titles:
        # Tokenize, remove punctuation at the end of each word, and filter stop words
        words.extend([word.rstrip(string.punctuation).lower() for word in title.split() if word.lower() not in stop_words])
    return Counter(words)

def plot_top_keywords(year, top_words, ax):
    """Plot the top keywords for a given year."""
    words, counts = zip(*top_words)
    ax.barh(words, counts, color='skyblue')
    ax.set_title(f"Top Keywords for ICLR {year}")
    ax.set_xlabel("Count")
    ax.set_ylabel("Keywords")
    ax.invert_yaxis()  # To display the keyword with the highest count at the top

def main():
    # Adjust this variable to display the desired number of top keywords
    num_keywords_to_display = 20
    
    # Extract titles for each year
    titles_2020 = extract_titles_from_file('../data/iclr2020.txt')
    titles_2021 = extract_titles_from_file('../data/iclr2021.txt')
    titles_2022 = extract_titles_from_file('../data/iclr2022.txt')
    titles_2023 = extract_titles_from_file('../data/iclr2023.txt')
    
    # Get word frequencies for each year
    word_freq_2020 = get_word_frequency(titles_2020)
    word_freq_2021 = get_word_frequency(titles_2021)
    word_freq_2022 = get_word_frequency(titles_2022)
    word_freq_2023 = get_word_frequency(titles_2023)
    
    # Get top N words for each year
    top_words_2020 = word_freq_2020.most_common(num_keywords_to_display)
    top_words_2021 = word_freq_2021.most_common(num_keywords_to_display)
    top_words_2022 = word_freq_2022.most_common(num_keywords_to_display)
    top_words_2023 = word_freq_2023.most_common(num_keywords_to_display)
    
    # Plotting
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))
    plot_top_keywords(2020, top_words_2020, axes[0][0])
    plot_top_keywords(2021, top_words_2021, axes[0][1])
    plot_top_keywords(2022, top_words_2022, axes[1][0])
    plot_top_keywords(2023, top_words_2023, axes[1][1])
    plt.tight_layout()
    plt.show()

main()
