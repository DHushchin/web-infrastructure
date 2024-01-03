FROM python:3.11-alpine
WORKDIR /app
RUN apk update && apk add build-base
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .