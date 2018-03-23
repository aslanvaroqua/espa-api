
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
WORKDIR /home/espadev/espa-api
COPY --from=application /home/espadev/espa-api /home/espadev/espa-api/
COPY --from=application /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

RUN pip install -e .[test]
COPY ./test/ ./test/
ENTRYPOINT ["pytest", "--cov=./"]
