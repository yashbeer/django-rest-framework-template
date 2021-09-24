# README #

### What is this repository for? ###

This repository is a boilerplate project written in **django** and **django-rest-framework.** It can serve as a starting point for any project which aims to create APIs in django.


### Features ###

1. Includes `core` and `user` app with following endpoints.

 - registering a new user
 - generating token for a user
 - fetching & updating the profile

2. Includes `flake8` linter

3. Written with TDD (Test Driven Development) approach



### How to set up? ###

```
docker-compose run app sh -c "python manage.py test && flake8"
```

### How to run? ###
```
docker-compose up -d
```