import os

config = {
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "youtube_playlist_id": os.getenv("YOUTUBE_PLAYLIST_ID"),
    "kafka": {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        "security.protocol": os.getenv("KAFKA_SECURITY_PROTOCOL", "sasl_ssl"),
        "sasl.mechanism": os.getenv("KAFKA_SASL_MECHANISM", "PLAIN"),
        "sasl.username": os.getenv("KAFKA_SASL_USERNAME"),
        "sasl.password": os.getenv("KAFKA_SASL_PASSWORD"),
    },
    "schema_registry": {
        "url": os.getenv("SCHEMA_REGISTRY_URL"),
        "basic.auth.user.info": os.getenv("SCHEMA_REGISTRY_BASIC_AUTH"),
    }
}