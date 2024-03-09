SHELL := /bin/bash

.PHONY: clean install run test docker-build docker-run

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

install:
	poetry install

run: install
	poetry run uvicorn ocr.main:app --reload

test:
	poetry run pytest

docker-build:
	docker build -t ocr-app .

docker-run: docker-build
	docker run -p 8000:8000 ocr-app
