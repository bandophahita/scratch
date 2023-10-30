requirements:
	poetry export --without-hashes --with dev -f requirements.txt > requirements.txt

sync:
	poetry install --with dev --sync

update_lock_only:
	poetry update --lock

update: update_lock_only 
	poetry install --with dev

.PHONY: requirements sync update update_lock_only
