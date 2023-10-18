import os
import requests
from bs4 import BeautifulSoup
import random

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Failed to fetch the webpage ({response.status_code})")
        return None

def find_links_and_tags(soup, subjects, prefix):
    found_links = []
    tags = []

    for subject in subjects:
        target_word = prefix + subject
        for tag in soup.find_all(string=lambda text: text and target_word in text.lower()):
            parent_tag = tag.parent
            if parent_tag.name == 'a' and parent_tag.get('href'):
                link = parent_tag.get('href')
                tag = parent_tag.get('data-ga-event-label')
                found_links.append(link)
                tags.append(tag)
    return found_links, tags

def download_file(url, target_filename, desired_filename):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{desired_filename}.tsv"
        target_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(target_filepath, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filename}')
        
    else:
        print(f"Error: Failed to download {desired_filename} ({response.status_code})")

def remove_random_lines(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    first_line = lines[0]  # Preserve the first line

    lines_to_remove = random.randint(0, min(5, len(lines) - 1))  # Ensure at least one line is kept
    remaining_lines = random.sample(lines[1:], max(len(lines) - 1 - lines_to_remove, 0))
    lines_to_keep = [first_line] + remaining_lines

    with open(output_file, 'w') as f:
        f.writelines(lines_to_keep)
    os.remove(input_file)
