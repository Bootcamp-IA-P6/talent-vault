from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str = "localhost:29092"
    kafka_topic: str = "testing"
    kafka_group_id: str = "talent-vault-consumer"

    mongo_host: str = "mongodb"
    mongo_port: int = 27017
    mongo_user: str = "admin"
    mongo_password: str = "admin"
    mongo_db: str = "talent_vault_raw"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "admin"
    postgres_password: str = "admin"
    postgres_db: str = "talent_vault"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_fragment_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
