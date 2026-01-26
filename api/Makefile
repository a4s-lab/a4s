# Variables

# Commands

### General Commands:
.PHONY: help
help: ## Display this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$|^### .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; { \
		if ($$0 ~ /^### /) { \
			printf "\n\033[1m%s\033[0m\n", substr($$0, 5); \
		} else if ($$0 ~ /^[a-zA-Z_-]+:.*?## /) { \
			printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2; \
		} \
	}'

### Deployment
.PHONY: dev
dev: ## Run the API server
	uv run --env-file .env fastapi dev app/server.py

### Development
.PHONY: format
format: ## Format code
	uv run ruff format

.PHONY: lint
lint: ## Run linting
	uv run ruff check --fix

### Testing
.PHONY: test
test: TEST_FILES ?= tests/unit
test: ## Run tests
	uv run pytest $(TEST_FILES)
