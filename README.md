# django-postgres-elasticsearch

If you're starting with **Part 2** or later, don't forget to run the following commands:

```bash
$ mkdir -p server/static
```

```bash
$ docker-compose up -d --build
```

```bash
$ docker-compose exec server python manage.py createsuperuser
```

```bash
$ docker-compose exec server \
    python manage.py loaddata \
        catalog/fixtures/wines.json \
        --app catalog \
        --format json
```