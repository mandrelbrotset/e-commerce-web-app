#!/bin/sh

/etc/init.d/nginx start
/etc/init.d/nginx status

exec "$@"
