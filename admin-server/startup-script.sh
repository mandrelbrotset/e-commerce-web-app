#!/bin/sh

/etc/init.d/nginx start
/etc/init.d/nginx status

printf "REST_API='%s/'\n" "${REST_API}" > config.py

exec "$@"
