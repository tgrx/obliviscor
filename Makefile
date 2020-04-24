HERE := $(shell pwd)
VENV := $(shell pipenv --venv)
PYTHONPATH := ${HERE}/src
TEST_PARAMS := --verbosity 2 --pythonpath ${PYTHONPATH}

ifeq ($(origin PIPENV_ACTIVE), undefined)
	PY := pipenv run
endif

DBCLIENT := $(shell which mysql) --user root --password
ifeq ($(ENV_FOR_DYNACONF), travis)
	DBCLIENT := $(shell which mysql) --user root
	PY :=
	TEST_PARAMS := --failfast --keepdb --verbosity 0 --pythonpath ${PYTHONPATH}
else ifeq ($(ENV_FOR_DYNACONF), heroku)
	# TODO: figure out what to do in that case
	DBCLIENT :=
	PY :=
endif

MANAGE := ${PY} python src/manage.py


.PHONY: format
format:
	${PY} isort --virtual-env ${VENV} --recursive --apply ${HERE}
	${PY} black ${HERE}


.PHONY: sh
sh:
	${MANAGE} shell


.PHONY: run
run: static
	${MANAGE} runserver


.PHONY: static
static:
	${MANAGE} collectstatic --noinput --clear -v0


.PHONY: migrations
migrations:
	${MANAGE} makemigrations


.PHONY: migrate
migrate:
	${MANAGE} migrate


.PHONY: resetdb
resetdb:
	${DBCLIENT} < ${HERE}/ddl/reset_db.sql


.PHONY: initdb
initdb: resetdb migrate


.PHONY: su
su:
	${MANAGE} createsuperuser


.PHONY: token
token:
	${MANAGE} drf_create_token $(TOKEN_USER)


.PHONY: test
test:
	ENV_FOR_DYNACONF=test \
	${PY} coverage run \
		src/manage.py test ${TEST_PARAMS} \
			applications \
			project \

	${PY} coverage report
	${PY} isort --virtual-env ${VENV} --recursive --check-only ${HERE}
	${PY} black --check ${HERE}


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

