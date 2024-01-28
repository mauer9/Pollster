# Pollster

## Introduction

Django poll app is a full featured polling app. You have to register in this
app to show the polls and to vote. If you already voted you can not vote again.
Only the owner of a poll can add poll , edit poll, update poll, delete poll,
add choice, update choice, delete choice and end a poll. If a poll is ended it
can not be voted. Ended poll only shows user the final result of the poll.
There is a search option for polls. Also user can filter polls by name,
publish date, and by number of voted. Pagination will work even after applying
filter.

✅Password validation
Dependencies:

- Python v3.11
- Django v4.2
- PostgreSQL 16

## Project Setup

download the code and install poetry dependencies

```bash
git clone https://github.com/mauer9/pollster.git
cd pollster
poetry install
```

migrate database

```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

create admin user using this command

```bash
poetry run python manage.py createsuperuser
```

run the app locally

```bash
poetry run python manage.py runserver
```

## Docker

Make sure you've installed Docker v24 or up, Docker Compos v2 or up
build and run the docker image

```bash
docker compose up
```
