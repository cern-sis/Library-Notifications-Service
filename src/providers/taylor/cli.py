import click
from utils import (
    configure_driver,
    get_url,
    download_files,
)

@click.command()
@click.option('--subject', prompt='Enter the subject', type=click.Choice(['all', 'chemistry', 'computer science', 'engineering', 'math', 'materials', 'physics', 'stats']))
@click.option('--directory', prompt='Enter the directory', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(subject, directory):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    driver = configure_driver(user_agent, directory)

    url = get_url(subject)
    if not url:
        print("Invalid subject selection")
        driver.quit()
        return

    download_files(driver, url, directory)

    driver.quit()

if __name__ == "__main__":
    main()
