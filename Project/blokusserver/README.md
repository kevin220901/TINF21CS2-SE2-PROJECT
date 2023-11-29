## Compose Blokus Game Application

### Use with Docker Environments

You can open this sample with Docker Desktop version 4.12 or later.


### Django application Blokus Game in Development

Project structure:
```
.
├── docker-compose.yaml
├── .env 
├── app
    ├── Dockerfile
    ├── requirements.txt
    ├── manage.py
    └── blokus
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        └── wsgi.py
        

```

[_docker-compose.yaml_](docker-compose.yaml)
```
services:
  web: 
    build:
      context: app
      target: dev-envs
    ports: 
      - '8000:8000'
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    env_file:
      - ./.env
    depends_on:
      - postgres_db
    
  postgres_db:
      image: postgres
      volumes:
        - postgres_data:/var/lib/postgresql/data
      environment:
        - POSTGRES_DB=${SQL_NAME}
        - POSTGRES_USER=${SQL_USER}
        - POSTGRES_PASSWORD=${SQL_PASSWORD}
        
      ports:
        - '5432:80'

  pgadmin:
    image: dpage/pgadmin4
    depends_on:
      - postgres_db
    ports:
      - 5555:80
    environment:
      - PGADMIN_DEFAULT_EMAIL=${PGADMIN_DEFAULT_EMAIL}
      - PGADMIN_DEFAULT_PASSWORD=${PGADMIN_DEFAULT_PASSWORD}
    restart: unless-stopped
volumes:
  postgres_data:
```

## Deploy with docker compose

```
$ docker compose up -d
```

## Application URL

After the application starts, navigate to `http://localhost:8000` in your web browser: Web-Application
<br/>
After the application starts, navigate to `http://localhost:5555` in your web browser: PgAdmin

## Login-Data PGAdmin and Database

Go to .env

## Stop and Remove Containers

```
$ docker compose down
```
