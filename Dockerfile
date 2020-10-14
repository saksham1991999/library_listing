FROM python:3

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN apt-get update

RUN apt-get -qq -y install binutils libproj-dev gdal-bin

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

#COPY . /code/
#WORKDIR /code/
#
#EXPOSE 8000