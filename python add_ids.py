import os
from bs4 import BeautifulSoup
import json
import hashlib

def generate_unique_key(path):
    """Generates a unique key from a file path using SHA-256."""
    return hashlib.sha256(path.encode('utf-8')).hexdigest()


def extract_content_from_html(html_file):
    """Extracts title and relevant content from an HTML file."""
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Extract the title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else 'No Title'

        # Extract relevant content (adjust as needed)
        content_parts = []

        # Extract text from <h> tags
        for h_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
           content_parts.append(h_tag.get_text(strip=True))
        # Extract text from <p> tags
        for p_tag in soup.find_all('p'):
           content_parts.append(p_tag.get_text(strip=True))
         # Extract text from div tags with classes that match cards
        for div_tag in soup.find_all('div', class_='sec-1-card'):
           content_parts.append(div_tag.get_text(strip=True))

         for div_tag in soup.find_all('div', class_='faq-item'):
            question_tag = div_tag.find(class_='faq-question')
            content_tag = div_tag.find(class_='faq-content')
            if question_tag:
                 content_parts.append(question_tag.get_text(strip=True))
            if content_tag:
                 content_parts.append(content_tag.get_text(strip=True))

        content = ' '.join(content_parts)

        return {"title": title, "content": content, "path": html_file}
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        return None


def create_search_index(directory):
    """Creates a search index from all HTML files in the specified directory."""
    search_index = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_file = os.path.join(root, file)
                 # Generate a unique key using the file path
                unique_key = generate_unique_key(html_file)
                page_data = extract_content_from_html(html_file)
                if page_data:
                    search_index[unique_key] = page_data

    return search_index


def save_search_index_to_file(search_index, output_file):
    """Saves the search index to a JavaScript file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('const searchIndex = ')
        json.dump(search_index, file, indent=4)
        file.write(';')

if __name__ == "__main__":
    target_directory = '.'  # Current directory or replace it with your folder path
    output_js_file = 'js/index.js'
    search_index = create_search_index(target_directory)
    save_search_index_to_file(search_index, output_js_file)
    print(f"Search index saved to {output_js_file}")