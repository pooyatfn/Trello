FROM postgres:16.2-bullseye

RUN apt-get update && \
    apt-get install postgresql-client --yes && \
    apt-get install --no-install-recommends --yes \
    tzdata \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /src

COPY dbconfig /etc/postgresql/
RUN chown -R postgres:postgres /etc/postgresql
RUN chmod -R 777 /etc/postgresql
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
