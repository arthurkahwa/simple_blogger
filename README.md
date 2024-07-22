simple_blogger demo
===================

Simple Blog application demonstrating using FastAPI to read and write data to a PostgreSQL containerized RDBMS and present it in a REST service.

# Running the application
## Start the Docker cotainer with database
Inthe the ```database``` folder
Start the Docker Container which hosts the PostgreSQL database engine

```shell
cd database
docker compose up --build -d
```

## Install Python Modules
In the ```pythonProject``` folder

```shell
pip install fastapi psycopg2 uvicorn 
```

## Start the development server
```shell
uvicorn main:app --reload
```

Once started, the server presents data at the address:
[http://localhost:8000](http://localhost:8000)
The API Swagger documentation can be accessed at [http://localhost:8000/docs](http://localhost:8000/docs) or alternatively at [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Basic Operations
#### Get All Posts
```shell
curl --location 'http://localhost:8000/posts/'
```

### Get a single post
```shell
curl --location 'http://localhost:8000/posts/1'
```

### Create a post
```shell
curl --location 'http://localhost:8000/posts/1' \
--header 'Content-Type: application/json' \
--data '{
        "title": "Created Post",
        "post": "Lorem ipsum dolor sit amet."
    }'
```

### Update a post
```shell
curl --location --request PUT 'http://localhost:8000/posts/1' \
--header 'Content-Type: application/json' \
--data '{
        "title": "Updated Post",
        "post": "dolor sit amet."
    }'
```

### Delete a post
```shell
curl --location --request DELETE 'http://localhost:8000/posts/2'
```