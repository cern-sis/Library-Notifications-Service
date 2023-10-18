import os
import requests
from bs4 import BeautifulSoup
import random

from functions import (
    get_page_content,
    find_links_and_tags,
    download_file,
    remove_random_lines
)

def main():
    print
    url = 'https://www.cambridge.org/core/services/librarians/kbart'
    response_text = get_page_content(url)

    if response_text:
        soup = BeautifulSoup(response_text, 'html.parser')

        prefix = 'cambridge ebooks and partner presses: 2023 '
        subjects = ['computer science', 'engineering', 'mathematics', 'physics', 'science and engineering', 'statistics']

        found_links, tags = find_links_and_tags(soup, subjects, prefix)

        for link, subject in zip(found_links, subjects):
            link2 = 'https://www.cambridge.org' + link
            download_file(link2, link.split('/')[-1], subject)

        subjectfiles = []
        for subject in subjects:
            subjectfiles.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), subject) + '.tsv')
        for subject in subjectfiles:
            output_file = subject.replace('.tsv', '_test.tsv')
            remove_random_lines(subject, output_file)
            print(f"Random lines removed from {subject} and saved as {output_file}")

if __name__ == "__main__":
    main()