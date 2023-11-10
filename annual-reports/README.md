# Annual Reports

## Installation
```
poetry install
docker-compose up -d

export DB_PASSWORD=annual
export DB_USER=annual
export DB_NAME=annual
export DB_HOST=localhost
export DB_PORT=5432
export CDS_TOKEN=ADD_TOKEN
```

## Run
### With specific years
```
poetry run  python src/cli.py -y 2022 -y 2023
```

### For all years
```
poetry run python src/cli.py
```
