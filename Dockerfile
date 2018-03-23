
# ==========+ Source Code dependencies +==========
FROM python:3.6-slim as application
RUN apt-get update && apt-get install -y gcc

RUN useradd espadev
WORKDIR /home/espadev/espa-api
COPY setup.py version.txt README.md /home/espadev/espa-api/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

COPY ./api/ /home/espadev/espa-api/api/
COPY ./run/ /home/espadev/espa-api/run/

ENV ESPA_CONFIG_PATH=/home/espadev/espa-api/run/config.ini \
    ESPA_API_EMAIL_RECEIVE="someone@somewhere.com" \
    ESPA_ENV="dev" \
    ESPA_MEMCACHE_HOST="memcached:11211" \
    ESPA_LOG_STDOUT=True

USER espadev
EXPOSE 8303 8304 8305
ENTRYPOINT ["uwsgi", "run/uwsgi.ini"]


# ==========+ Unit testing dependencies +==========
FROM python:3.6-slim  as tester
RUN apt-get update && apt-get install -y gcc

WORKDIR /home/espadev/espa-api
COPY . /home/espadev/espa-api/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e . \
    && pip install -e .[test]
ENTRYPOINT ["pytest", "--cov=./"]
