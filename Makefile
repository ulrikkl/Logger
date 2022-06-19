.PHONY: help start stop build

help: ## Show this help menu
	@echo "Usage: make [TARGET ...]"
	@echo ""
	@grep --no-filename -E '^[a-zA-Z_%-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-15s %s\n", $$1, $$2}'

start: ## Start docker
	@docker-compose up -d;

stop: ## Stop docker
	@docker-compose stop;

build: ## Build docker image
	@bash deployment/nginx/init_ssl.sh
	@docker-compose up --build -d;
