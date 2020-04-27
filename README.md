[![Build Status](https://travis-ci.org/tgrx/obliviscor.svg?branch=master)](https://travis-ci.org/tgrx/obliviscor)
[![codecov](https://codecov.io/gh/tgrx/obliviscor/branch/master/graph/badge.svg)](https://codecov.io/gh/tgrx/obliviscor)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# OBLIVISCOR

Nunquam obliviscar

## TL;DR

Just visit [obliviscor.herokuapp.com](https://obliviscor.herokuapp.com).

API: [DRF](https://obliviscor.herokuapp.com/api/v1/), [Swagger](https://obliviscor.herokuapp.com/api/swagger/).

API Token:
```
POST /api/obtain_auth_token/
username=username
password=password
```

```
Authorization: Token 0123456789abcdef
```

## Docker

The app requires some settings.

One can add them
1. either via `config/.secrets.yaml` (see [settings.yaml](https://github.com/tgrx/obliviscor/blob/master/config/settings.yaml) for examples)
1. either via ENVs - they MUST be prefixed with `OBLIVISCOR_`.

If you want to send mails,
please configure the email settings
via secrets/envs.

These are required:
1. `EMAIL_FROM`: sender email for all mails
1. `EMAIL_HOST`: name says it all
1. `EMAIL_HOST_PASSWORD`: name says it all
1. `EMAIL_HOST_USER`: name says it all
1. `EMAIL_PORT`: name says it all
1. `EMAIL_USE_SSL`: 0 or 1
1. `EMAIL_USE_TLS`: 0 or 1
