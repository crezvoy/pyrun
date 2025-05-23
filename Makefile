PYTHON_VERSION ?= $(shell cat .python-version)
VERSION ?= $(shell git rev-parse --short=8 HEAD)
REGISTRY ?=

include .env

.PHONY: all check build test login deploy run clean check-typing check-lint

test: .venv
	uv run pytest -n auto tests

check-typing: .venv
	uv run mypy pyrun tests

check-lint: .venv
	uv run ruff check pyrun tests

format: .venv
	uv run ruff check -n --fix pyrun tests
	uv run ruff format -n pyrun tests

check: test check-typing check-lint

.venv:
	uv sync --frozen

build: .venv
	docker buildx build  --build-arg PYTHON_VERSION=$(PYTHON_VERSION) --load -t pyrun:$(VERSION) .

run: build
	docker run --privileged -p 8080:8080 pyrun:$(VERSION) --rm --name pyrun \

login:
	gcloud auth login

proj:
	gcloud config set project $(GCLOUD_PROJECT_ID)

deploy: requirements.txt
	gcloud run deploy pyrun --source . \
        --allow-unauthenticated \
		--region $(GCLOUD_REGION) \
		--project $(GCLOUD_PROJECT_ID)

requirements.txt:
	uv export --no-hashes --no-header --no-dev --format requirements-txt > requirements.txt

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf .ruff_cache
