# Library Notifications Service

## System Requirements

- pyenv
- Python >=3.11
- pre-commit
- Poetry

## Setup

Before you start, ensure you have `pyenv` installed on your system. If not, you can install it using Homebrew (for macOS):

```bash
$ brew update
$ brew install pyenv
```

For Linux, you can use the command below:

```bash
$ curl https://pyenv.run | bash
```

For Windows, please refer to the official [pyenv-win](https://github.com/pyenv-win/pyenv-win) repository.

Once `pyenv` is installed, you can install Python 3.11:

```bash
$ pyenv install 3.11.0
$ pyenv global 3.11.0
```

Next, install `pre-commit`:

```bash
$ pip install pre-commit
```

And finally, install `poetry`:

```bash
$ curl -sSL https://install.python-poetry.org | python -
```

## Installing the Project

1. Clone the repository to your local machine:

    ```bash
    $ git clone https://github.com/cern-sis/Library-Notifications-Service.git
    ```

2. Navigate to the project directory:

    ```bash
    $ cd Library-Notifications-Service
    ```

3. Install the dependencies using `poetry`:

    ```bash
    $ poetry install
    ```

4. Install pre-commit hooks:
    ```bash
    $ pre-commit install
    ```


## Usage

After installing, you can use the CLI as follows:

### Newsletter

```bash
$ python -m src.cli newsletter
```

## Supported Arguments

1. Subjects domain
    - Get the latest(weekly) updates from backoffice and send the notifications for those present in the catalouge.
    - Format: `value:scheme`

2. Title
    - Title of the notification
    - Format: `'Information Technology'`

3. Target Group
    - Egroup identifier for sending targetted notifications.
    - Format: `'library-newsletter-notif-it'`

## Adding a new query to send notifications

Add a new container with the required arguments (subject, title, target) in the below mentioned format in `cronjob.yml` in qa/prod environment.

```yaml
-  name: <lns-subject>
   image: registry.cern.ch/cern-sis/library-notifications-service
   envFrom:
    - secretRef:
        name: lns-creds
    - configMapRef:
        name: lns-cfg
    args:
    - '--subjects'
    - '<value:scheme>'
    - '--title'
    - '<string>'
    - '--target'
    - '<e-group-identifier>'
```

## Repository Structure

1. api.py - Module containing calls to library catalouge, backoffice and notifications instances.
2. cli.py - Main module conatining the supported command line arguments.
3. utils.py - Module containing helper methods to manipulate data.


## Example

```
python -m src.cli newsletter --subjects '65*:' --subjects '005*:UDC' --title 'Administration/Management' --target 'library-newsletter-notif-management'

python -m src.cli newsletter --subjects '52*:' --title 'Astronomy/Astrophysics' --target 'library-newsletter-notif-astrophysics'

python -m src.cli newsletter --subjects '62*:' --title 'Engineering/Technology' --target 'library-newsletter-notif-engineering'

python -m src.cli newsletter --subjects '004*:' --subjects '006*:' --subjects '007*:' --subjects '005*:DEWEY' --title 'Information Technology' --target 'library-newsletter-notif-it'

python -m src.cli newsletter --subjects '51*:' --title 'Mathematics' --target 'library-newsletter-notif-math'

python -m src.cli newsletter --subjects '53*:' --title 'Physics' --target 'library-newsletter-notif-physics'
```
