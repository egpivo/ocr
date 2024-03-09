SHELL := /bin/bash

.PHONY: clean install run test

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

install:
	poetry install

run: install
	poetry run uvicorn ocr.main:app --reload

test:
	poetry run pytest
