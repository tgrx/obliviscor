HERE := $(shell pwd)
MYSQL := $(shell which mysql) --user root --password
PIPENV := $(shell which pipenv)
VENV := $(shell pipenv --venv)

ifeq ($(origin PIPENV_ACTIVE), undefined)
	PY := pipenv run
endif

ifeq ($(ENV_FOR_DYNACONF), travis)
	MYSQL := $(shell which mysql) --user root
endif


.PHONY: format
format:
	${PY} isort --virtual-env ${VENV} --recursive --apply ${HERE}
	${PY} black ${HERE}


.PHONY: run
run: static
	${PY} python src/manage.py runserver


.PHONY: runa
runa: static
	PYTHONPATH="${HERE}/src" ${PY} uvicorn project.asgi:application


.PHONY: static
static:
	${PY} python src/manage.py collectstatic --noinput --clear -v0


.PHONY: migrations
migrations:
	${PY} python src/manage.py makemigrations


.PHONY: migrate
migrate:
	${PY} python src/manage.py migrate


.PHONY: resetdb
resetdb:
	${MYSQL} < ${HERE}/ddl/reset_db.sql


.PHONY: initdb
initdb: resetdb migrate


.PHONY: su
su:
	${PY} python src/manage.py createsuperuser


.PHONY: test
test:
	ENV_FOR_DYNACONF=test \
	${PY} coverage run \
		src/manage.py test -v2 \
			applications \
			project \

	${PY} coverage report
	${PY} black --check ${HERE}
	${PY} isort --virtual-env ${VENV} --recursive --check-only ${HERE}


.PHONY: report
report:
	${PY} coverage html --directory=${HERE}/htmlcov --fail-under=0
	open "${HERE}/htmlcov/index.html"


.PHONY: venv
venv:
	pipenv install --dev


.PHONY: clean
clean:
	${PY} coverage erase
	rm -rf htmlcov
	find . -type d -name "__pycache__" | xargs rm -rf
	rm -rf ./.static/

