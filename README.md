# Foodgram

![Foodgram workflow](https://github.com/MuggleSkin/foodgram-project/workflows/Foodgram_workflow/badge.svg)

Foodgram is a projects that allows you to share your recipes with community and learn the new ones.

Running at:

[Foodgram site](http://185.181.11.219/)

## Getting Started

[Install docker engine](https://docs.docker.com/engine/install/)

[Install docker-compose](https://docs.docker.com/compose/install/)

Download this github project on your local machine or remote server. 

Create ".env" file in the root directory of your project and fill it with required environment variables:

```
DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=your_db_name
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
DB_HOST=db
DB_PORT=5432
NGINX_HOST=127.0.0.1
NGINX_PORT=80
```

if you want your app to run locally - leave NGINX_HOST as it is in example,
otherwise provide your server's public ip or domain name

### Deploying

Open terminal to create and start new containers with docker-compose:

```
sudo docker-compose pull && sudo docker-compose up -d
```

(Optionally) Unpack fixtures_media.zip inside your container to get the test pictures.

```
sudo docker-compose exec web unzip ../fixtures_media.zip -d ../
```

and fill your database with test data from fixtures.json:

```
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

Create superuser to be able to moderate resources:

```
sudo docker-compose exec web python manage.py createsuperuser
```

and follow the further instructions.


## Testing the service

Your service is available on

```
http://NGINX_HOST:NGINX_PORT/
```

Admin page is available at

```
http://NGINX_HOST:NGINX_PORT/admin/
```

You can inspect database using db service:

```
sudo docker-compose exec db psql your_db_name your_postgres_user
```

## Built With

[Yandex Praktikum](https://praktikum.yandex.ru) - Online educational service
