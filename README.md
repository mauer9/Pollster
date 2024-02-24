# Pollster

Pollster is a full featured polling app. You have to register in this app to
show the polls and to vote. You can vote for several choices. Only the owner of
a poll can edit poll, update poll, delete poll, add choices, update choices,
delete choices. Ended poll only shows user the final result of the poll. You
can sort polls by heading, date and number of votes. Pagination will work even
after applying filter.

- ✅PostgreSQL
- ✅Redis
- ✅Registration, Authentication
- ✅Password validation

Dependencies:

- Python v3.11
- Django v4.2
- PostgreSQL v16
- Redis v7

## Project Setup

### Docker

Make sure you've installed Docker v24 or up, Docker Compos v2 or up.

build and run the docker image

```bash
docker compose up
```

### Manual

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
