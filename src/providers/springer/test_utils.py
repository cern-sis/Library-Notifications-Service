import os 
import pytest
from bs4 import BeautifulSoup
from utils import get_page_content, find_links_and_tags, download_file

@pytest.mark.vcr()
def test_page_content_valid():
    response = get_page_content('https://adminportal.springernature.com/metadata/kbart')
    assert response.status_code == 200

@pytest.mark.vcr()
def test_page_content_invalid():
    response = get_page_content('https://adminportal.springernature.com/metadata/errkbart')
    assert response.status_code == 404  

@pytest.mark.vcr
def test_found_links():
    url = 'https://adminportal.springernature.com/metadata/kbart'
    response = get_page_content(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    founds_links = find_links_and_tags(soup, ['engineering'], 'springer ', ' ebooks 2023')
    assert len(founds_links) == 1

@pytest.mark.vcr
def test_found_no_links():
    url = 'https://adminportal.springernature.com/metadata/kbart'
    response = get_page_content(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    founds_links = find_links_and_tags(soup, ['lhcb'], 'springer ', ' ebooks 2023')
    assert len(founds_links) == 0

@pytest.mark.vcr
def test_download_file(tmp_path):
    url = 'https://adminportal.springernature.com/metadata/kbart/Springer_Global_Springer_Computer_Science_eBooks_2023_English+International_2023-08-01.txt'
    desired_filename = 'computer science'
    target_filepath = str(tmp_path)
    download_file(url, desired_filename, target_filepath)
    expected_filepath = os.path.join(target_filepath, f"{desired_filename}.tsv")
    assert os.path.exists(expected_filepath)
    assert os.path.getsize(expected_filepath) > 0
