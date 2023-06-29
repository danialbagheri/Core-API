# pull official base image
FROM python:3.9.14-alpine


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk add --no-cache --virtual .build-deps gcc musl-dev

# # install python3-dev
# RUN apk update \
#     && apk add --virtual .build-deps gcc libc-dev

# RUN apk update && apk add postgresql-dev python3-dev

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libc-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
#     && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
#     && pip install Pillow \
#     && apk del build-deps

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY src/ /usr/src/app/
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install -r /usr/src/app/requirements.txt
