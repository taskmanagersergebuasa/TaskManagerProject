# TaskManagerProject# TaskManagerProject

## Purpose

The objective of this project is to create a database to compare the Simplon training offer with other training courses available on the "Compte Formation" website.

On the one hand, the Simplon site is scraped to recover the elements necessary for the comparison.
On the other hand, an extraction of the elements available on the "Compte Formation" website makes it possible to constitute a common database to make comparisons.

It includes:
- Tables are created with SQLAlchemy
- An API (FastAPI) without authentication (with token-based authentication g)
- The database will be hosted on Azure.
- (Scraping of the Simplon site must be automated and carried out weekly via Azure.)
- (The API will be dockerized, and deployed on Azure ACI.)

- (The procedure for building a Postgres SQL database on Azure and procedure for importing data.)


## Dependencies:
- poetry
- pandas
- scrapy
- sqlalchemy
- fastapi
- uvicorn

(- azure CLI
- azure ml CLI
- psql)

## Setup

1. Create virtual environement and install requirements:

```bash

poetry install

```

2. Create .env file in path /TaskManagerProject/formationscraper/.env using this template 

IS_POSTGRES=0  # 0 or 1 : 0 = sqlite database / 1 = postgredatabase
DATABASE_SQLITE=sqlite:////....../database.db # indiquer le chemin vers la bdd
DB_USERNAME=
DB_PASSWORD=
DB_HOSTNAME=
DB_PORT=
DB_NAME=


3. To create a sqlite database, execute this command :

first, make sure the .env is adjusted for the sqlite database

then :
```bash
scrapy crawl formationspider
```


(To create the Olist database, execute these commands:
```bash
chmod +x ./database/azure_postgres/create_postgres.sh
./database/azure_postgres/create_postgres.sh

chmod +x ./database/azure_postgres/create_tables.sh
./database/azure_postgres/create_tables.sh

chmod +x ./database/azure_postgres/import_postgres.sh
./database/azure_postgres/import_postgres.sh
```)

## Launch the API

```bash
uvicorn formation scraper.main:app --reload
```


1. Get your token:

```bash
(poetry run python -m api.utils)
```

2. Update model_name in ./api/launch_app.sh and then you can execute it


