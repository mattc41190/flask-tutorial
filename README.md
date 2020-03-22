# Flask Tutorial - Flaskr

__*This is not a real application. It is a tutorial application that demonstrates how you can make a simple flask application.__

## What is this?

This is the code repo for the excellent _Flaskr_ application. It is capable of doing amazing things.

## Why make this?

To change your life!

## How do I use it?

- Register
- Log in
- Create your own posts
- Read others posts

## How do I contribute to it?

### Get it

- `git clone <repo-addr>`

### Dev IT 

- Needs `venv` & `python3`

- `make venv`
- `make dev_db`
- `make dev`
- `<code something>`
- `<test your thing>`
- `make test`

## How do I build and distribute it?

Note, `desired location should have `waitress` and `venv` already.

See: https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/#deploy-to-production

- `make clean dist`
- `cp dist/flaskr-X.X.X-py3-none-any.whl </desired/location>`
- `pip install flaskr-X.X.X-py3-none-any.whl`
- init db if needed
	- `export FLASK_APP=flaskr && flask init-db`
- set up secret if needed
	- `echo "SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'" >> <venv>/var/flaskr-instance/config.py`
- Serve app
	- `waitress-serve --port 80 --call 'flaskr:create_app'`

## Resources

- https://docs.python.org/3/library/functools.html

## To Dos

- Read: https://packaging.python.org/tutorials/packaging-projects/
- Read: https://docs.python.org/3/library/functools.html
- Read Docs: PyTest
- Read: https://robertheaton.com/2014/02/09/pythons-pass-by-object-reference-as-explained-by-philip-k-dick/
- Check Out: https://advancedbeginners.substack.com/

## Questions and Mysteries

- `__init__`, modules, and file paths in general in Python are tough for me to understand at the moment.