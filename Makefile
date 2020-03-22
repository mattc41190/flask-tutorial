.PHONY: venv
venv:
	source .venv/bin/activate

.PHONY: dev
dev:
	export FLASK_APP=flaskr && export FLASK_ENV=development && flask run

.PHONY: dev_db
dev_db:
	export FLASK_APP=flaskr && export FLASK_ENV=development && flask init-db

.PHONY: test
test:
	pytest

.PHONY: dist
dist: test
	python setup.py bdist_wheel

.PHONY: clean
clean:
	rm -rf .coverage .pytest_cache htmlcov build dist