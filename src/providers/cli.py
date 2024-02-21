import subprocess
import click

@click.command()
@click.option('--publisher', prompt='Enter the publisher', type=click.Choice(['cambridge', 'springer', 'taylor']))
def main(publisher):

    cli_paths = {
    'cambridge': "src/providers/cambridge/cli.py",
    'springer': "src/providers/springer/cli.py",
    'taylor': "src/providers/taylor/cli.py"
    }

    script = cli_paths.get(publisher)
    subprocess.run(["python", script])

if __name__ == "__main__":
    main()
