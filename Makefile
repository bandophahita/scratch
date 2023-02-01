requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

sync:
	poetry install --with dev --sync

poetryupdate:
	poetry update --with dev

update: poetryupdate requirements

.PHONY: requirements sync poetryupdate update
