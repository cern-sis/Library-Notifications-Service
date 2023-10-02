import click

from .providers import library_newsletter


@click.group()
def main():
    pass


main.add_command(library_newsletter.cli, "newsletter")

if __name__ == "__main__":
    main()
