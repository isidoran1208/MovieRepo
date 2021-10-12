FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /Movies
WORKDIR /Movies
ADD requirements.txt /Movies/
RUN pip install -r requirements.txt
ADD . /Movies/