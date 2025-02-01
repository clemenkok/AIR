import requests
import time

# Function to read titles from a text file
def read_titles(file_path):
    with open(file_path, 'r') as file:
        titles = [line.strip() for line in file if line.strip()]
    return titles

# Function to get DOI from CrossRef
def get_doi(title):
    url = f"https://api.crossref.org/works?query.title={title}&rows=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get('message', {}).get('items', [])
        if items:
            return items[0].get('DOI')
    return None

# Function to get citations from OpenCitations
def get_citations(doi):
    url = f"https://opencitations.net/index/api/v1/citations/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Main process
def main(file_path):
    titles = read_titles(file_path)
    for title in titles:
        print(f"Processing: {title}")
        doi = get_doi(title)
        if doi:
            print(f"DOI found: {doi}")
            citations = get_citations(doi)
            if citations:
                print(f"Citations for '{title}':")
                for citation in citations:
                    print(citation)
            else:
                print(f"No citations found for '{title}'.")
        else:
            print(f"DOI not found for '{title}'.")
        time.sleep(1)  # Respectful delay between API requests

if __name__ == "__main__":
    main('titles.txt')
