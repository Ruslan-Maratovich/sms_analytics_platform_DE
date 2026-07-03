FROM clickhouse/clickhouse-server:25.3
MAINTAINER RuslanKhaliullin
USER root

COPY init.sql /docker-entrypoint-initdb.d/
COPY ddl/ /ddl/
USER clickhouse