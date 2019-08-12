#!/bin/sh

/etc/init.d/nginx start
/etc/init.d/nginx status

printf "REST_API='http://%s/'\n" "${REST_API}" >> config.py
printf "API_KEY='%s'\n" "${API_KEY}" >> config.py

exec "$@"
