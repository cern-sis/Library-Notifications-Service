from bs4 import BeautifulSoup
import click

from utils import (
    get_page_content,
    find_links_and_tags,
    download_file
)

@click.command()
@click.option('--subject', prompt='Enter the subject', type=click.Choice(['chemistry and materials science', 'computer science', 'engineering', 'mathematics and statistics', 'physics and astronomy']))
@click.option('--directory', prompt='Enter the directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(subject,directory):
    url = 'https://adminportal.springernature.com/metadata/kbart'
    response = get_page_content(url)

    if response:
        soup = BeautifulSoup(response.text, 'html.parser')
        prefix = 'springer '
        suffix = ' ebooks 2023'
        subjects = [subject]
        found_links = find_links_and_tags(soup, subjects, prefix, suffix)
        for link, subject in zip(found_links, subjects):
            full_link = 'https://adminportal.springernature.com' + link
            download_file(full_link, subject, directory)

if __name__ == "__main__":
    main()
