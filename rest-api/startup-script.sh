#!/bin/sh

/etc/init.d/nginx start
/etc/init.d/nginx status

printf "DB_HOST='%s'\n" "${DB_HOST}" >> config.py
printf "DB_PORT='%s'\n" "${DB_PORT}" >> config.py

exec "$@"
