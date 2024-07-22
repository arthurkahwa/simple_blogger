FROM postgres:latest
LABEL authors="arthur.kahwa_at~googlemail.com"

COPY 01_init.sh ./docker-entrypoint-initdb.d/
COPY init /usr/src/

RUN chmod a+r ./docker-entrypoint-initdb.d/*