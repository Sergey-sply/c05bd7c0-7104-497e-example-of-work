from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class FastAPISettings(EnvBaseSettings):
    DOMAIN_HOST: str
    DOMAIN_PORT: int | None = None


class NatsBrokerSettings(EnvBaseSettings):
    NATS_URL: str
    NATS_PORT: int

    # JetStream
    js_stream: str
    js_subject: str
    js_durable: str

    @property
    def NATS_BROKER_URL(self):
        return f"nats://{self.NATS_URL}:{self.NATS_PORT}"


class DBSettings(EnvBaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class RedisSettings(EnvBaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None
    REDIS_DB: int = 0
    REDIS_MAX_CONN: int = 5
    REDIS_SOCKET_TIMEOUT: int
    REDIS_CONNECT_TIMEOUT: int

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


class Settings(
    NatsBrokerSettings,
    DBSettings,
    RedisSettings,
    FastAPISettings
):
    jwt_algorithm: str = "RS256"
    jwt_public_key: str | None = None
    jwt_secret: str | None = None

settings = Settings()