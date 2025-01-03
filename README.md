# Deployed application

The deployed version of the application can be accessed in the following URL: https://my-fav-app-04d416c5eb24.herokuapp.com/careers/

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

## 3. Run linter

```sh
flake8 --ignore=E501,W503,W504 app
```

## 4. Run tests

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