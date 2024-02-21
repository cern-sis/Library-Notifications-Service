import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def configure_driver(user_agent, download_directory):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--headless")
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version='114.0.5735.90').install()), options=options)
    return driver

def get_url(subject):
    subject_urls = {
        'all': "https://www.taylorfrancis.com/collections/sci-technetbase/wb057?context=ubx",
        'chemistry': "https://www.taylorfrancis.com/collections/chemistrynetbase/wb063?context=ubx",
        'computer science': "https://www.taylorfrancis.com/collections/computersciencenetbase/wb058?context=ubx",
        'engineering': "https://www.taylorfrancis.com/collections/engnetbase/wb004?context=ubx",
        'math': "https://www.taylorfrancis.com/collections/mathnetbase/wb021?context=ub",
        'materials': "https://www.taylorfrancis.com/collections/materialsnetbase/wb032?context=ubx",
        'physics': "https://www.taylorfrancis.com/collections/physicsnetbase/wb048?context=ubx",
        'stats': "https://www.taylorfrancis.com/collections/statsnetbase/wb020?context=ubx",
    }
    return subject_urls.get(subject)

def download_files(driver, url, download_directory):
    driver.get(url)
    time.sleep(5)  # Page loading time

    # Find the button by its ID
    download_button = driver.find_element(By.CSS_SELECTOR, '#download-link\ gtm-collection-download')
    download_button.click()

    max_wait_time = 5  # Maximum wait time in seconds
    current_wait_time = 0
    while not any(fname.endswith('.crdownload') for fname in os.listdir(download_directory)):
        if current_wait_time > max_wait_time:
            break
        time.sleep(1)
        current_wait_time += 1
