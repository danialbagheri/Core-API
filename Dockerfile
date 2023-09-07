# pull official base image
FROM python:3.9.14-alpine


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev libc-dev \
    && apk add postgresql postgresql-dev \
    && apk add jpeg-dev zlib-dev libjpeg libffi-dev cairo-dev pango-dev gdk-pixbuf-dev
#     && apk del build-deps

# install dependencies
RUN pip install --upgrade pip

# copy project
COPY src/ requirements.txt /usr/src/app/

RUN mkdir /usr/src/app/static_root \
    && mv /usr/src/app/dashboard_static /usr/src/app/static_root \
    && pip install -r /usr/src/app/requirements.txt
