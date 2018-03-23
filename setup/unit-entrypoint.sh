#!/bin/bash

# Enable Montior mode (required for fg)
set -o monitor

# TODO: Hopefully, someday, unit allows startup configuration...
sudo /usr/sbin/unitd --no-daemon --control \
          "unix:${NGINX_UNITD_SOCK}" &

sudo curl -X PUT -d @${NGINX_UNITD_START_CONF} \
    --unix-socket ${NGINX_UNITD_SOCK} \
    http://localhost/

fg %1 # TODO: this is unfortunate...
