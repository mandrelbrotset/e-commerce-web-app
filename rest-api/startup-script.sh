#!/bin/sh

/etc/init.d/nginx start
/etc/init.d/nginx status

printf "DB_HOST='%s'\n" "${DB_HOST}" >> config.py
printf "DB_USERNAME='%s'\n" "${DB_USERNAME}" >> config.py
printf "DB_PASSWORD='%s'\n" "${DB_PASSWORD}" >> config.py
printf "DB_NAME='%s'\n" "${DB_NAME}" >> config.py
printf "DB_PORT='%s'\n" "${DB_PORT}" >> config.py
printf "API_KEY='%s'\n" "${API_KEY}" >> config.py

exec "$@"
