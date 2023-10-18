import os
import requests
from bs4 import BeautifulSoup
import click

from functions import (
    get_page_content,
    find_links_and_tags,
    download_file
)

@click.command()
@click.option('--subject', prompt='Enter the subject', type=click.Choice(['computer science', 'engineering', 'mathematics', 'physics', 'science and engineering', 'statistics']))
def main(subject):
    url = 'https://www.cambridge.org/core/services/librarians/kbart'
    response_text = get_page_content(url)

    if response_text:
        soup = BeautifulSoup(response_text, 'html.parser')

        prefix = 'cambridge ebooks and partner presses: 2023 '
        subjects = [subject]

        found_links, tags = find_links_and_tags(soup, subjects, prefix)

        for link, subject in zip(found_links, subjects):
            link2 = 'https://www.cambridge.org' + link
            download_file(link2, link.split('/')[-1], subject)
    process_subject(subject)

def process_subject(subject):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file1_path = os.path.join(script_dir, f"{subject}.tsv")
    file2_path = os.path.join(script_dir, f"{subject}_test.tsv")

    unique_lines = find_unique_lines(file1_path, file2_path)

    click.echo("New releases:")
    for line in unique_lines:
        click.echo(line)

def find_unique_lines(file1_path, file2_path):
    unique_lines = []

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = set(file1.readlines())
        lines2 = set(file2.readlines())
        unique_lines = lines1.difference(lines2)

    return unique_lines

if __name__ == "__main__":
    main()