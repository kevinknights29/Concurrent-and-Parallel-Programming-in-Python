# Official postgres image with custom initialization scripts
# URL: https://hub.docker.com/_/postgres
FROM postgres:latest

# Copy initializations scripts
ADD scripts/ /docker-entrypoint-initdb.d/
