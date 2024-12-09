# How to run the project

## 1. Environment variables

Rename the `.env.template` file to `.env` and set the variables according to your environment.

## 2. Run Docker services

```sh
docker compose up
```

```sh
docker exec -it application python manage.py migrate
```

Ther server should be running on [http://localhost:8000/careers/](http://localhost:8000/careers/)

## 3. Run tests

```sh
docker exec -it application coverage run manage.py test
```

```sh
docker exec -it application coverage report -m
```

or

```sh
docker exec -it application coverage html
```