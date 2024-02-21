import pytest
from utils import get_page_content, find_links_and_tags, download_file
from bs4 import BeautifulSoup
import os 

@pytest.mark.vcr()
def test_page_content_valid():
    response = get_page_content('https://www.cambridge.org/core/services/librarians/kbart')
    assert response.status_code == 200

@pytest.mark.vcr()
def test_page_content_invalid():
    response = get_page_content('https://www.cambridge.org/core/services/librarians/kbartWontWork')
    assert response.status_code == 404 

@pytest.mark.vcr
def test_found_links():
    url = 'https://www.cambridge.org/core/services/librarians/kbart'
    response = get_page_content(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    found_links = find_links_and_tags(soup, ['computer science'], 'cambridge ebooks and partner presses: 2023 ')
    assert len(found_links) == 1

@pytest.mark.vcr
def test_found_no_links():
    url = 'https://www.cambridge.org/core/services/librarians/kbart'
    response = get_page_content(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    found_links = find_links_and_tags(soup, ['isolde'], 'cambridge ebooks and partner presses: 2023 ')
    assert len(found_links) == 0

@pytest.mark.vcr
def test_download_file(tmp_path):
    url = 'https://www.cambridge.org/core/services/aop-cambridge-core/kbart/create/bespoke/717854B1C18FD5D0B882344E83E6F52B'
    desired_filename = 'computer science'
    target_filepath = str(tmp_path)
    download_file(url, desired_filename, target_filepath)
    expected_filepath = os.path.join(target_filepath, f"{desired_filename}.tsv")
    assert os.path.exists(expected_filepath)
    assert os.path.getsize(expected_filepath) > 0
