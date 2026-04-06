.PHONY: build run test docker-build docker-run lint release clean help

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "ENCT enchub Makefile"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build enchub binary for current OS
	@echo "Building enchub..."
	@mkdir -p dist
	@cd src/enchub && go build -o ../../dist/enchub .
	@echo "✓ Binary: ./dist/enchub"

run: build ## Build and run enchub locally
	@echo "Starting enchub on port 8081..."
	./dist/enchub

test: ## Run all tests (engine + enchub)
	@echo "Running tests..."
	@cd src/engine && go test -v ./... && cd ../..
	@cd src/enchub && go test -v ./... && cd ../..
	@echo "✓ All tests passed"

lint: ## Run go vet on all modules
	@echo "Running lint checks..."
	@cd src/engine && go vet ./...
	@cd ../enchub && go vet ./...
	@echo "✓ Lint checks passed"

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	@docker build -t enct/enchub:latest -t enct/enchub:v0.3.0 .
	@echo "✓ Docker image built: enct/enchub:latest"

docker-run: docker-build ## Build and run with Docker Compose
	@echo "Starting enchub with Docker Compose..."
	@docker-compose up

docker-stop: ## Stop Docker Compose services
	@docker-compose down
	@echo "✓ Docker Compose stopped"

release: ## Build cross-platform releases with goreleaser
	@echo "Building releases with goreleaser..."
	@goreleaser release --clean
	@echo "✓ Releases built in dist/"

release-snapshot: ## Build snapshot releases (without publishing)
	@echo "Building snapshot releases..."
	@goreleaser release --snapshot --clean
	@echo "✓ Snapshot releases built in dist/"

clean: ## Remove build artifacts
	@echo "Cleaning up..."
	@rm -rf dist/
	@docker-compose down --remove-orphans || true
	@echo "✓ Cleaned"

.PHONY: build run test docker-build docker-run docker-stop lint release release-snapshot clean help
