import re
import string
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def extract_descriptions_from_file(filename):
    descriptions = []
    
    with open(filename, 'r') as file:
        content = file.readlines()

    # Regular expression to extract the description
    pattern = r'<li><a href=".*?">(.*?)</a></li>'

    for line in content:
        match = re.search(pattern, line)
        if match:
            descriptions.append(match.group(1))
    
    return descriptions

def generate_word_cloud(descriptions):
    # Convert list of descriptions to a single string
    text = ' '.join(descriptions)
    
    # Generate the word cloud
    wordcloud = WordCloud(background_color="white", max_words=100, contour_width=3, contour_color='steelblue')
    wordcloud.generate(text)
    
    # Plot the word cloud
    plt.figure(figsize=(10, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    
    return text

def generate_latex_table(text, output_filename):
    # List of common stop words
    stop_words = set([
        "and", "in", "the", "from", "by", "on", "with", "as", "for", "to",
        "is", "of", "at", "an", "a", "or", "that", "this", "it", "are", "be",
        "was", "were", "will", "have", "has", "had", "not", "but", "if", "which"
    ])
    
    # Tokenize the text, remove punctuation at the end of each word
    words = [word.rstrip(string.punctuation).lower() for word in text.split() if word.lower() not in stop_words]
    
    # Count occurrences of each word
    word_count = Counter(words)
    
    # Sort the word counts in descending order
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    # Start the LaTeX table
    latex_table = []
    latex_table.append("\\begin{table}[h]")
    latex_table.append("\\centering")
    latex_table.append("\\begin{tabular}{|l|r|}")
    latex_table.append("\\hline")
    latex_table.append("Keyword & Number of Occurrences \\\\")
    latex_table.append("\\hline")
    
    # Add data to the LaTeX table
    for word, count in sorted_word_count:
        latex_table.append(f"{word} & {count} \\\\")
        latex_table.append("\\hline")
    
    # End the LaTeX table
    latex_table.append("\\end{tabular}")
    latex_table.append("\\caption{Keyword Occurrences}")
    latex_table.append("\\end{table}")
    
    # Write the LaTeX table to a file
    with open(output_filename, 'w') as f:
        for line in latex_table:
            f.write(line + '\n')

def main():
    filename = input("Enter the filename (e.g., iclr2023.txt): ")
    base_name = filename.split('.')[0]
    
    descriptions = extract_descriptions_from_file(filename)
    text_from_wordcloud = generate_word_cloud(descriptions)
    
    # Save the word cloud image
    wordcloud_img_filename = base_name + "_wordcloud.png"
    wordcloud = WordCloud(background_color="white", max_words=100, contour_width=3, contour_color='steelblue')
    wordcloud.generate(text_from_wordcloud)
    wordcloud.to_file(wordcloud_img_filename)
    
    # Generate and save the LaTeX table
    latex_filename = base_name + "_counts.tex"
    generate_latex_table(text_from_wordcloud, latex_filename)
    
    print(f"Word cloud saved to: {wordcloud_img_filename}")
    print(f"LaTeX table saved to: {latex_filename}")

main()
