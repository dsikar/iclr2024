import re
from collections import Counter

def basic_tokenize(text):
    """Tokenizes the text by splitting it on spaces and removing non-alphabetic tokens."""
    tokens = text.lower().split()
    return [t.strip('.,!?()[]{}:;\"\'') for t in tokens if t.isalpha()]

def extract_papers_by_year(text_content):
    """Parse the provided text content to extract papers grouped by year."""
    year_pattern = re.compile(r"## ICLR (\d{4}) \(\d+\)")
    years = year_pattern.findall(text_content)
    split_content = year_pattern.split(text_content)[1:]
    year_paper_mapping = {}
    for i in range(0, len(split_content), 2):
        year = int(split_content[i])
        papers = [paper.strip() for paper in split_content[i + 1].strip().split("\n") if paper]
        year_paper_mapping[year] = papers
    return year_paper_mapping

# Loading the content of the files
with open("/home/daniel/git/iclr2024/data/ICLR2020-2023_Out-of-Distribution_Papers.txt", "r") as file:
    out_of_distribution_papers = file.read()
with open("/home/daniel/git/iclr2024/data/ICLR2020-2023_Robustness_Papers.txt", "r") as file:
    robustness_papers = file.read()

# Extracting papers by year for both categories
out_of_distribution_by_year = extract_papers_by_year(out_of_distribution_papers)
robustness_by_year = extract_papers_by_year(robustness_papers)

# Combining titles from both categories
combined_papers_by_year = {}
for year in range(2020, 2024):
    combined_papers = out_of_distribution_by_year.get(year, []) + robustness_by_year.get(year, [])
    combined_papers_by_year[year] = combined_papers

# Tokenizing titles and generating keywords by year
combined_keywords_by_year = {}
for year, papers in combined_papers_by_year.items():
    all_keywords_yearly = []
    for paper in papers:
        tokens = basic_tokenize(paper)
        all_keywords_yearly.extend(tokens)
    combined_keywords_by_year[year] = Counter(all_keywords_yearly)

# Identifying emerging and declining keywords
emerging_keywords = set(combined_keywords_by_year[2023]) - set(combined_keywords_by_year[2020])
declining_keywords = set(combined_keywords_by_year[2020]) - set(combined_keywords_by_year[2023])

print("Emerging Keywords:", emerging_keywords)
print("Declining Keywords:", declining_keywords)
