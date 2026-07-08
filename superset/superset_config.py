import os

# Generate a secure key using: openssl rand -base64 42
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "YOUR_OWN_RANDOM_GENERATED_SECRET_KEY")
# clickhousedb+connect://default:default123@clickhouse01:8123/sms
# Bind to all interfaces inside the container
SUPERSET_WEBSERVER_ADDRESS = "0.0.0.0"
SUPERSET_WEBSERVER_PORT = 8088

# Add feature flags or custom configs here if needed
FEATURE_FLAGS = {
    "EMBEDDED_SUPERSET": True,
    "DASHBOARD_NATIVE_FILTERS": True,
    "ENABLE_TEMPLATE_PROCESSING": True
}