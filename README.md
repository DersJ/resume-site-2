# resume-site-2

## Source code for my personal website:

The site is built on django 3.2 with a Postgres database.

[See it live.](http://www.andersjuengst.com)


## Deployment

Deployed on Linode with Docker.

Followed Docker's official [quickstart for django with docker-compose](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/django)

To run, `.env` file must be created with environment variables. Docker compose reads these vars and passes into containers.