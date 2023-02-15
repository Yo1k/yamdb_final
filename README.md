# YaMDb

<a href="https://docs.python.org/3.7/">
<img src="https://img.shields.io/badge/Python-3.7-FFE873.svg?labelColor=4B8BBE" 
alt="Python requirement">
</a>

<a href="https://flake8.pycqa.org/en/5.0.4/">
<img src="https://img.shields.io/badge/flake8-5.0-E4D00A.svg?labelColor=555">
</a>

<a href="https://docs.pytest.org/en/6.2.x/contents.html">
<img src="https://img.shields.io/badge/pytest-6.2-E4D00A.svg?labelColor=555">
</a>

![workflow status](https://github.com/Yo1k/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## About
API service that aggregates reviews from users on various artworks 
(henceforth, 'title' is used interchangeably for artworks). Artworks are 
separated on categories ('Books', 'Films', etc). Also, each artwork can 
have 
several genres ('Tales', 'Roman', etc).

Only administrator can manage 'titles', 'categories', and 'genres'.

Authenticated users can write reviews and comments for titles and other 
people's reviews, respectively. A review consists from user's text and 
score for specific title. User can write only one review for specific title.
Score is an integer number from 1 to 10. Artworks have rating calculated as 
the average of all scores of specific artwork.

Anonymous users can only view resource materials.

The service is deployed at: http://91.239.27.130/

Tech stack: \
[Django 2.2](https://docs.djangoproject.com/en/2.2/),
[Django REST framefowrk 3.12](https://www.django-rest-framework.org)


## Running the project in Docker

Clone this git repository. \
Set `./infra/.env` variables using as template `./infra/sample.env`.

Before starting, [install Docker Compose](https://docs.docker.com/compose/install/) if you do not have 
it. Below it is assumed that
[Docker's repositories](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)
are set up. By default, the Docker daemon always runs as the `root` user. If you do not want to 
preface the docker command with `sudo` (or `su -`) see
[this](https://docs.docker.com/engine/install/linux-postinstall/). The following assumes that commands beginning with `#` are run as the `root` user. Start Docker daemon with command:

```shell
# service docker start
```
For further `docker compose` commands change directory to the `./infra` or add this fragment to e commands: `docker compose -f ./infra/docker-compose.yaml <other_comands>`.

### Run containers

To create and run Docker containers run (`-d` to run services in the background):
```shell
# docker compose up -d
```
and to stop and delete containers:
```shell
# docker compose down -v
```

To find out `<CONTAINER ID>` of running containers run:
```shell
# docker container ls
```

### Setup web-service database and other files in containers

After starting the container you need to make migrations inside a container with `web` service (name image `yo1k/api_yamdb:v1.0`):
```shell
# docker compose exec web python manage.py migrate
```

There is Django command `fill_in_db` to fill in DB by prepared data from CSV-files (place of files: `./api_yamdb/static/data/`):
```shell
# docker compose exec web python manage.py fill_in_db
```

To create superuser:
```shell
# docker compose exec web python manage.py createsuperuser
```

To create folder with all Django static files:
```shell
# docker compose exec web python manage.py collectstatic --no-input 
```

To make database backups of the project running in the Docker use:
```shell
# docker compose exec web python manage.py dumpdata > ./data/backups/<name backup>.json
```
`./infra/data/backups/` &mdash; is dedicated folder for database backups. Files in this folder are persistent regardless of whether docker containers are running or shut down.

To restore database from backup files run:
```shell
# docker compose exec web python manage.py loaddata ./data/backups/<name backup>.json
```


## Endpoints

Documentation of endpoints is placed in file
`./api_yamdb/static/redoc.yaml `
To watch it in convenient way you can view it on `/redoc` endpoint after 
run the service or import yaml file to
[swagger editor](https://editor.swagger.io/) online resource.

**authorisation**

* `api/v1/auth/signup/` (POST): creates new _user_ by his credentials and 
  sends him `conformation_code`
* `api/v1/auth/token/` (POST): creates jwt-token after get valid `username` 
  and `conformation_code`


**categories**

attributes:\
`slug`: slug

* `api/v1/categories/` (GET, POST): gets list of all categories or creates 
  new category
* `api/v1/categories/{slug}/` (DELETE): deletes a category by its `slug`

**genres**

attributes:\
`slug`: slug

* `api/v1/genres/` (GET, POST): gets list of all genres or creates 
  new genre
* `api/v1/genres/{slug}/` (DELETE): deletes a genre by its `slug`

**titles**

attributes:\
`titles_id`: integer

* `api/v1/titles/` (GET, POST): gets list of all titles or creates new 
  title
* `api/v1/titles/{titles_id}/` (GET, PUT, PATCH, DELETE):
  gets, modifies or deletes a title by its `titles_id`

**reviews**

attributes:\
`titles_id`: integer\
`review_id`: integer

* `api/v1/titles/{titles_id}/reviews/` (GET, POST): gets list of all 
  reviews for a title with `id=titles_id` or creates new post for the title
* `api/v1/titles/{titles_id}/reviews/{reivew_id}/` (GET, PATCH, DELETE): 
  gets, modifies or deletes a review by its `reivew_id` for a title with 
  `id=titles_id`

**comments**

attributes:\
`titles_id`: integer\
`review_id`: integer\
`comment_id`: integer

* `api/v1/titles/{titles_id}/reviews/{reivew_id}/comments/` (GET, POST): gets 
  list 
  of all comments for a review with `id=review_id` or creates new comment 
  for the review
* `api/v1/titles/{titles_id}/reviews/{reivew_id}/comments/{comment_id}/` 
  (GET, PATCH, DELETE): 
  gets, modifies or deletes a comment by its `comment_id` for a review with 
  `id=review_id`

**users**

attributes:\
`username`: string

* `api/v1/users/` (GET, POST): gets list of all users or creates new user
* `api/v1/users/{username}/` (GET, PATCH, DELETE): gets, modifies or 
  deletes a user by its `username`
* `api/v1/users/me/` (GET, PATCH): gets, modifies current authorized user