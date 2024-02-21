import click
from bs4 import BeautifulSoup
from utils import (
    get_page_content,
    find_links_and_tags,
    download_file
)

@click.command()
@click.option('--subject', prompt='Enter the subject', type=click.Choice(['computer science', 'engineering', 'mathematics', 'physics', 'science and engineering', 'statistics']))
@click.option('--directory', prompt='Enter the directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(subject,directory):
    url = 'https://www.cambridge.org/core/services/librarians/kbart'
    response = get_page_content(url)

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        prefix = 'cambridge ebooks and partner presses: 2023 '
        subjects = [subject]
        found_links = find_links_and_tags(soup, subjects, prefix)
        for link, subject in zip(found_links, subjects):
            full_link = 'https://www.cambridge.org' + link
            download_file(full_link, subject, directory)

if __name__ == "__main__":
    main()


