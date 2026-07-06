FROM apache/superset:3.1.0

# Switch to root to install system dependencies and pip packages
USER root

# Install required database drivers (e.g., PostgreSQL, MySQL, ClickHouse)
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

    
RUN python -m pip install --no-cache-dir \
    psycopg2-binary \
    clickhouse-connect

# Copy custom configuration file into the container
COPY superset_config.py /app/pythonpath/superset_config.py
COPY init_superset.sh /
COPY ./dashboards/*.zip /app/superset/dashboards/
RUN chmod +x /init_superset.sh
# Switch back to the non-root superset user for safety

USER superset

ENTRYPOINT ["/init_superset.sh"]
