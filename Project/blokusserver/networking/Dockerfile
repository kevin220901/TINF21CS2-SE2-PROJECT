FROM --platform=$BUILDPLATFORM python:3.12.0-alpine3.17 AS builder
EXPOSE 5555
WORKDIR /app 
COPY requirements.txt /app
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev --no-cache
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["blokuslauncher.py"]

FROM builder as dev-envs

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["blokuslauncher.py"]