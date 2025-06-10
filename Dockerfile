FROM python:3.12.4
RUN apt-get upgrade


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    CPLUS_INCLUDE_PATH=/usr/include/gdal \
    C_INCLUDE_PATH=/usr/include/gdal

RUN apt-get update

RUN apt-get update \
  && apt-get install -y gettext \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gcc \
  && apt-get install -y libgdal-dev \
  && apt-get install -y libpango-1.0-0 \
  && apt-get install -y libharfbuzz0b \
  && apt-get install -y libpangoft2-1.0-0 \
  && apt-get install -y python3-pip \
  && apt-get install -y libgdal-dev \
  && apt-get install -y gdal-bin \
  && apt-get install -y python3-gdal \
  && apt-get install -y python3-distutils \
  && apt-get install -y build-essential  \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

COPY start.sh pyproject.toml poetry.lock ./
COPY app ./app


RUN pip install  --upgrade pip setuptools==57.5.0 
RUN pip install poetry
RUN poetry env activate
RUN poetry add  GDAL==`gdal-config --version`
RUN /bin/bash -c pip wheel --no-cache-dir --use-pep517 gdal==3.2.2
RUN poetry update  
CMD sh -c chmod 777 ./start.sh & ./start.sh

