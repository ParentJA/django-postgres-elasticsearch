# django-postgres-elasticsearch

If you're starting with **Part 2** or later, don't forget to run the following commands:

```bash
# Create a static directory
$ mkdir -p server/static
```

```bash
# Build all of the Docker containers
$ docker-compose up -d --build
```

```bash
# Create a superuser
$ docker-compose exec server python manage.py createsuperuser
```

```bash
# Load all of the fixture data
$ docker-compose exec server \
    python manage.py loaddata \
        catalog/fixtures/wines.json \
        --app catalog \
        --format json
```

Loading the fixture data will take a long time (at least 10 minutes) because Django is copying 150,000+ records. Each record spawns an update to the `catalog_winesearchword` table as well as updates the `search_vector` field on the `catalog_wine` table. This all happens in a single transaction. After you do this once, you should consider dumping the database so that you can restore it later if you need to.

First, run the following command to dump the database:

```sh
$ docker-compose exec database pg_dump -U perusable -f perusable.sql -F plain perusable
```

The database backup file will be on the container and you'll need to copy it to your host machine.

First, find the database's container ID:

```sh
$ docker container ls
```

Next, use the container ID to copy the database dump to your host:

```sh
# This will copy the file to the host directory you are running the command from
# Replace <container_id> with your own
$ docker cp <container_id>:perusable.sql .
```

Delete the backup file from your container:

```sh
$ docker-compose exec database bash
root@<container_id>:/# rm perusable.sql
root@<container_id>:/# exit
```

Alternatively, you can dump the database to `stdout` and pipe the output into a file on your host machine. Use `gzip` to compress the data:

```sh
$ docker-compose exec database pg_dump -U perusable perusable | gzip > perusable.gz
```

To restore, first copy the backup from your host to the container:

```sh
# This will copy the file to the /data directory in the container
# Replace <container_id> with your own
$ docker cp perusable.sql <container_id>:/data
```

Then, drop the database:

```sh
$ docker-compose exec database dropdb perusable -U perusable
```

Finally, restore the database:

```sh
# Specifying the file will create the database from scratch
$ docker-compose exec database pg_restore -U perusable -f /data/perusable.sql
```

> **NOTE**
> 
> In practice, restoring the database with `pg_restore` takes just as long (if not longer) as loading the fixtures through Django.