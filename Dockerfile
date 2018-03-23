
# ==========+ Source Code dependencies +==========
FROM python:3.6-slim as application
RUN apt-get update && apt-get install -y gcc

WORKDIR /usr/local/src
COPY setup.py version.txt README.md /usr/local/src/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

RUN useradd espadev
COPY ./api/ /home/espadev/espa-api/api/
COPY ./run/ /home/espadev/espa-api/run/
WORKDIR /home/espadev/espa-api

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
COPY --from=application /home/espadev/espa-api /home/espadev/espa-api
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e . \
    && pip install -e .[test]
ENTRYPOINT ["nose2", "--log-level", "ERROR", "--fail-fast", "--with-coverage"]
