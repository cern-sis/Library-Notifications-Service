import requests
import structlog
import os

logger = structlog.get_logger()

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectionError as err:
        logger.error(err)
        return response
    except requests.exceptions.HTTPError as err:
        logger.error(err)
        return response

def find_links_and_tags(soup, subjects, prefix, suffix):
    found_links = []
    for subject in subjects:
        target_word = prefix + subject + suffix
        for tag in soup.find_all(string=lambda text: text and target_word in text.lower()):
            parent_tag = tag.parent
            if parent_tag.name == 'a' and parent_tag.get('href'):
                link = parent_tag.get('href')
                found_links.append(link)
            else:
                continue
    return found_links

def download_file(url, desired_filename, target_filepath):
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{desired_filename}.tsv"
        file_path = os.path.join(target_filepath, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filename}')
    else:
        print(f"Error: Failed to download {desired_filename} ({response.status_code})")
