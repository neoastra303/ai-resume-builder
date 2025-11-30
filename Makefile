# Makefile for AI Resume Builder

# Variables
PYTHON := python
PIP := pip
MANAGE := $(PYTHON) manage.py
DOCKER := docker
COMPOSE := docker-compose

# Default target
.PHONY: help
help: ## Show this help message
	@echo "AI Resume Builder - Development Commands"
	@echo ""
	@echo "Usage:"
	@echo "  make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install Python dependencies
	$(PIP) install -r requirements.txt

.PHONY: install-dev
install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 isort

.PHONY: run
run: ## Run the development server
	$(MANAGE) runserver --settings=resume_builder.settings.development

.PHONY: migrate
migrate: ## Run database migrations
	$(MANAGE) migrate

.PHONY: makemigrations
makemigrations: ## Create database migrations
	$(MANAGE) makemigrations

.PHONY: test
test: ## Run tests
	$(MANAGE) test

.PHONY: coverage
coverage: ## Run tests with coverage
	$(MANAGE) test --keepdb --parallel --debug-mode
	coverage report -m

.PHONY: lint
lint: ## Run code linting
	flake8 .

.PHONY: format
format: ## Format code with Black
	black .

.PHONY: sort
sort: ## Sort imports with isort
	isort .

.PHONY: check
check: ## Check code quality
	flake8 .
	black --check .
	isort --check-only .

.PHONY: clean
clean: ## Clean Python cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

.PHONY: docker-up
docker-up: ## Start Docker containers
	$(COMPOSE) up -d

.PHONY: docker-down
docker-down: ## Stop Docker containers
	$(COMPOSE) down

.PHONY: docker-build
docker-build: ## Build Docker images
	$(COMPOSE) build

.PHONY: docker-logs
docker-logs: ## View Docker logs
	$(COMPOSE) logs -f

.PHONY: docs
docs: ## Build documentation
	$(COMPOSE) -f docker-compose.docs.yml up --build

.PHONY: superuser
superuser: ## Create a superuser
	$(MANAGE) createsuperuser

.PHONY: collectstatic
collectstatic: ## Collect static files
	$(MANAGE) collectstatic --noinput

.PHONY: shell
shell: ## Open Django shell
	$(MANAGE) shell

.PHONY: dbshell
dbshell: ## Open database shell
	$(MANAGE) dbshell