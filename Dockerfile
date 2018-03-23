
# ==========+ Source Code dependencies +==========
FROM python:3.5 as baselayer

WORKDIR /usr/local/src
COPY setup.py version.txt README.md /usr/local/src/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

RUN useradd espadev
COPY . /home/espadev/espa-api
WORKDIR /home/espadev/espa-api

ENV ESPA_CONFIG_PATH=/home/espadev/espa-api/run/config.ini \
    ESPA_API_EMAIL_RECEIVE="someone@somewhere.com" \
    ESPA_ENV="dev" \
    ESPA_MEMCACHE_HOST="memcached:11211" \
    ESPA_LOG_STDOUT=True

USER espadev
ENTRYPOINT ["python3"]

# ==========+ Server dependencies +==========
FROM nginx/unit:0.7-python3.5 as wsgi
COPY --from=baselayer /home/espadev/espa-api /home/espadev/espa-api
RUN apt-get update \
    && apt-get install sudo
RUN useradd www-espa-api
RUN useradd nginx \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
COPY run/unit.json /usr/local/unit.json
COPY setup/unit-entrypoint.sh /entrypoint.sh
ENV NGINX_UNITD_SOCK=/var/run/unitd/control.unit.sock \
    NGINX_UNITD_START_CONF=/usr/local/unit.json
EXPOSE 80 8300
USER nginx
ENTRYPOINT ["/entrypoint.sh"]


# ==========+ Unit testing dependencies +==========
FROM python:3.6 as tester
COPY --from=baselayer /home/espadev/espa-api /home/espadev/espa-api
RUN pip install -e .[test]
ENTRYPOINT ["nose2", "--log-level", "ERROR", "--fail-fast", "--with-coverage"]
