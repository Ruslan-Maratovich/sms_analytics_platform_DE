FROM apache/superset:latest

# Switch to root to install system dependencies and pip packages
USER root

# Install required database drivers (e.g., PostgreSQL, MySQL, ClickHouse)
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    psycopg2-binary \
    mysqlclient \
    clickhouse-connect


# Copy custom configuration file into the container
COPY superset_config.py /app/pythonpath/superset_config.py
COPY init_superset.sh /
RUN chmod +x /init_superset.sh
# Switch back to the non-root superset user for safety

USER superset

ENTRYPOINT ["/init_superset.sh"]