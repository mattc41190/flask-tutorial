.PHONY: dev
dev:
	export FLASK_APP=flaskr && export FLASK_ENV=development && flask run

.PHONY: dev_db
dev_db:
	export FLASK_APP=flaskr && export FLASK_ENV=development && flask init-db