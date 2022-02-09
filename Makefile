all:
	@echo "COMMANDS IMPLEMENTED"
	@echo ""
	@echo "########################################################################################################################"
	@echo "[SESSION] build image"
	@echo "make build-img .................................. build imgs WITH CACHE (using Dockerfile)"
	@echo ""
	@echo "########################################################################################################################"
	@echo "[SESSION] Launch"
	@echo "make up ......................................... docker-compose up -d"
	@echo "make stop ....................................... docker-compose stop"
	@echo "make down ....................................... docker-compose down"
	@echo "make app ........................................ run container app"
	@echo "make rm ......................................... remove all exited containers and all dangling volumes"
	@echo ""
	@echo "########################################################################################################################"
	@echo "[SESSION] DB"
	@echo "make db-phoenix ................................ drop all public schema and re-create tables"
	@echo "make db-create ................................. create database (if not exists)"
	@echo "make db-create-tables .......................... create all tables (if not exists)"
	@echo "make db-setup .................................. create database and create all tables"
	@echo "make db-enter .................................. enter on postgres container"
	@echo ""
	@echo "########################################################################################################################"
	@echo "[SESSION] Processing"
	@echo "make tests ..................................... run tests"
	@echo "make io-download ............................... download files"
	@echo "make io-unzip .................................. unzip all files"
	@echo "make io-create-jsons ........................... create jsons"
	@echo "make io-download-and-unzip ..................... download and unzip files"
	@echo "make engine-company ............................ load company data to db"
	@echo "make engine-company-tax-regime ................. load company tax regime data to db"
	@echo "make engine-company-root ....................... load company root data to db"
	@echo "make engine-company-root-simples ............... load company root simples data to db"
	@echo "make engine-partners ........................... load partners data to db"
	@echo "make engine-main ............................... load [company, company root, partners] data to db"
	@echo ""

build-img:
	@echo "---------------------------------------"
	@echo "CREATING IMAGE"
	@echo ""
	@docker build -t dados_publicos:1.0 .
	@echo ""
	@echo "IMAGE CREATED"
	@echo "---------------------------------------"

up:
	@echo "---------------------------------------"
	@echo "docker-compose up -d"
	@docker-compose up -d
	@echo ""

stop:
	@echo "---------------------------------------"
	@echo "docker-compose stop"
	@docker-compose stop
	@echo ""

down:
	@echo "---------------------------------------"
	@echo "docker-compose down"
	@docker-compose down
	@echo ""

app: up
	@echo "compose-up run app container"
	@docker-compose run --rm app
	@echo ""

rm: down
	@echo ""
	@echo ""
	@echo "remove all stopped containers"
	command docker ps -aqf status=exited | xargs -r docker rm
	@echo ""
	@echo ""
	@echo "remove all dangling volumes"
	@# The dangling filter matches on all volumes not referenced by any containers
	command docker volume ls -qf dangling=true | xargs -r docker volume rm
	@echo ""

db-create: up
	@echo "PHOENIX"
	@docker-compose run app python -c "from src.db_models.utils import create_db; create_db()"
	@echo ""

db-create-tables: up
	@echo "Creating tables"
	@docker-compose run app python -c "from src.db_models.utils import create_or_drop_all_tables; create_or_drop_all_tables(cmd='create')"
	@echo ""

db-setup: up
	@echo "SETUP"
	@echo "sleeping 40 seconds in order to postgres start-up"
	@sleep 40
	@echo "Creating db"
	@docker-compose run app python -c "from src.db_models.utils import create_db, create_or_drop_all_tables; create_db();create_or_drop_all_tables(cmd='create')"
	@echo ""

db-phoenix: up
	@echo "PHOENIX"
	@docker-compose run app python -c "from src.db_models.utils import phoenix; phoenix()"
	@echo ""

db-enter: up
	@docker exec -i postgres psql -U postgres

tests: up
	@echo "compose-up run app & [PYTEST]"
	@docker-compose run app python -m pytest
	@echo ""

io-download: up
	@echo "compose-up run app container & [DOWNLOAD]"
	@docker-compose run app python src/io/download.py
	@echo ""

io-unzip: up
	@echo "compose-up run app container & [UNZIP]"
	@docker-compose run app python src/io/unzip.py
	@echo ""
	@echo "[CREATE JSONS]"
	@docker-compose run app python src/io/create_jsons_from_csv.py

io-create-jsons: up
	@echo "[CREATE JSONS]"
	@docker-compose run app python src/io/create_jsons_from_csv.py


io-download-and-unzip: up
	@echo "compose-up run app container & [DOWNLOAD]"
	@docker-compose run app python src/io/download.py
	@echo ""
	@echo "------------------------"
	@echo "sleep for 30 seconds to take a breath"
	@sleep 30
	@echo ""
	@echo "------------------------"
	@echo "[UNZIP]"
	@docker-compose run app python src/io/unzip.py
	@echo ""
	@echo "[CREATE JSONS]"
	@docker-compose run app python src/io/create_jsons_from_csv.py

engine-company: up
	@echo "compose-up run app container & [ENGINE COMPANY]"
	@docker-compose run app python src/engine/company.py
	@echo ""

engine-company-tax-regime: up
	@echo "compose-up run app container & [ENGINE COMPANY TAX REGIME]"
	@docker-compose run app python src/engine/company_tax_regime.py
	@echo ""

engine-company-root: up
	@echo "compose-up run app container & [ENGINE COMPANY ROOT]"
	@docker-compose run app python src/engine/company_root.py
	@echo ""

engine-company-root-simples: up
	@echo "compose-up run app container & [ENGINE COMPANY ROOT SIMPLES]"
	@docker-compose run app python src/engine/company_root_simples.py
	@echo ""

engine-partners: up
	@echo "compose-up run app container & [ENGINE PARTNERS]"
	@docker-compose run app python src/engine/partners.py
	@echo ""

engine-ref-date: up
	@echo "compose-up run app container & [ENGINE REF DATE]"
	@docker-compose run app python src/engine/ref_date.py
	@echo ""

engine-main: up
	@echo "compose-up run app container & engine main"
	@docker-compose run app python src/engine/main.py
	@echo ""
