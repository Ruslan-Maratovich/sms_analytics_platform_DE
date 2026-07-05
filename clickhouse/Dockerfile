FROM clickhouse/clickhouse-server:25.3
MAINTAINER RuslanKhaliullin
USER root

COPY ./ddl/init.sql /docker-entrypoint-initdb.d/
COPY ddl/ /ddl/
USER clickhouse