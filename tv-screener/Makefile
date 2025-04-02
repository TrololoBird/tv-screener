install:
	pip install -r requirements.txt

openapi:
	python -m tv_screener.cli generate --market crypto --out openapi.yaml --json

validate:
	python -m tv_screener.cli validate openapi.yaml

sdk:
	python -m tv_screener.cli sdk --spec openapi.yaml --languages python typescript-fetch

models:
	python -m tv_screener.cli generate-models --input-json data/crypto.json

test:
	pytest

html:
	python -m tv_screener.cli generate-html openapi.yaml

all:
	make openapi
	make html

coverage:
	pytest --cov=tv_screener --cov-report=term-missing