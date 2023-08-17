import time
import sys
import re
from scholarly import scholarly

def extract_title_from_line(line):
    # Use regex to extract the title
    pattern = r'<li><a href=".*?">(.*?)</a></li>'
    match = re.search(pattern, line)
    return match.group(1) if match else None

def search_google_scholar(title):
    time.sleep(1)  # Introduce a delay of 1 second before making a query
    search_query = scholarly.search_pubs(title)
    try:
        publication = next(search_query)
        return publication
    except StopIteration:
        print("No results found for:", title)
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: script_name.py <filename>")
        return
    
    filename = sys.argv[1]
    
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        title = extract_title_from_line(line)
        if title:
            print(f"Searching for: {title}")
            result = search_google_scholar(title)
            
            if result:
                print("\nTitle:", result.bib.get('title'))
                print("Authors:", result.bib.get('author'))
                print("URL:", result.bib.get('url'))
                print("Year:", result.bib.get('year'))
                print('-'*50)

if __name__ == "__main__":
    main()
