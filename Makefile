.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "; printf "Usage: make [target]\n\n"} \
		/^##@/ {printf "\n%s\n", substr($$0, 5)} \
		/^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

##@ Development

.PHONY: format
format: ## Format code with ruff
	uv run ruff format

.PHONY: lint
lint: ## Check code with ruff
	uv run ruff check --fix

.PHONY: setup-dev
setup-dev: ## Setup development environment
	uv run pre-commit install

##@ Docker (Development)

.PHONY: dev-up
dev-up: ## Start dev services
	docker build -t a4s-personal-assistant:latest -f agents/personal-assistant/Dockerfile .
	docker compose -f compose.dev.yml up -d --build

.PHONY: dev-down
dev-down: ## Stop dev services
	docker compose -f compose.dev.yml down

##@ Docker (Production)

.PHONY: up
up: ## Start production services
	docker build -t a4s-personal-assistant:latest -f agents/personal-assistant/Dockerfile .
	docker compose up -d --build

.PHONY: down
down: ## Stop production services
	docker compose down
