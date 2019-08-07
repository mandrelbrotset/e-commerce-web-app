docker-compose -f admin-server/docker-compose.yml -f web-server/docker-compose.yml -f database/docker-compose.yml -f rest-api/docker-compose.yml -f docker-compose.override.yml build --force-rm
docker-compose -f admin-server/docker-compose.yml -f web-server/docker-compose.yml -f database/docker-compose.yml -f rest-api/docker-compose.yml -f docker-compose.override.yml up
