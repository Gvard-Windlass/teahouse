# Teahouse

Practice project written with django 4.1.1, styled using bootstrap 5.2.2

Images generated using [Craiyon](https://www.craiyon.com/) and [Stable Diffusion
Online](https://stablediffusionweb.com/).

## Working with project
To run project, use Docker

### running with sqlite database
build image:
```
docker build --tag teahouse-demo .
```

create container and run init script to create tables and demo data:
```
docker run -d \
    -p 8000:8000 \
    --name teahouse-local \
    -e DJANGO_SECRET_KEY="django-insecure"
    teahouse-demo
docker exec teahouse-local /app/init.sh
```

attach container:
```
docker attach teahouse-local
```

Then go to [localhost:8000](http://localhost:8000/)

### running with postgresql (compose)
create and start containers:
```
docker compose up
```

run init script to create tables and demo data:
```
docker compose exec server /app/init.sh
```

Then go to [localhost:8000](http://localhost:8000/)

### running with postgresql (manual)
build image:
```
docker build --tag teahouse-demo .
```

prepare volumes and network:
```
docker volume create postgres
docker volume create postgres_config
docker network create postgresnet
```

create postgres container:
```
docker run -d \
    -v postgres:/var/lib/postgresql/data \
    -v postgres_config:/etc/postgresql/15/main
    -p 5432:5432 \
    --network postgresnet \
    --name postgresdb \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -e POSTGRES_DB=teahouse \
    postgres:15
```

create server container and run init script to create tables and demo data:
```
docker run -d \
    -p 8000:8000 \
    --name teahouse-server \
    --network postgresnet \
    -e DJANGO_CONFIGURATION=TeahousePostgres \
    -e DB_HOST=postgresdb \
    -e DB_PASSWORD=mysecretpassword \
    -e DJANGO_SECRET_KEY="django-insecure" \
    teahouse-demo
docker exec teahouse-server /app/init.sh
```

attach server container:
```
docker attach teahouse-server
```

Then go to [localhost:8000](http://localhost:8000/)

## Screenshots
![Home page](screenshots/home.png?raw=true "Home page")
![Article page](screenshots/articles.png?raw=true "Article page")
![Products page](screenshots/products.png?raw=true "Products page")
![Product detail page](screenshots/product-detail.png?raw=true "Product detail page")
![Cart page](screenshots/cart.png?raw=true "Cart page")
![Profile page](screenshots/profile.png?raw=true "Profile page")
