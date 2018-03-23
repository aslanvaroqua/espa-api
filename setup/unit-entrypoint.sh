#!/bin/bash

# TODO: Hopefully, someday, unit allows startup configuration...
sudo /usr/sbin/unitd --no-daemon --control \
          "unix:${NGINX_UNITD_SOCK}" &

sleep 3
curl -X PUT -d @${NGINX_UNITD_START_CONF} \
    --unix-socket ${NGINX_UNITD_SOCK} \
    http://localhost/

fg $! # TODO: this is unfortunate...
