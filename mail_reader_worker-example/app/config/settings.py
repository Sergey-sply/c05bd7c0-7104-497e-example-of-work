from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


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

class RedisSettings(EnvBaseSettings):
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASS: str | None = None
    REDIS_DB: int = 0
    REDIS_MAX_CONN: int = 5
    REDIS_SOCKET_TIMEOUT: int
    REDIS_CONNECT_TIMEOUT: int

    # REDIS_DATABASE: int = 1
    # REDIS_USERNAME: int | None = None
    # REDIS_TTL_STATE: int | None = None
    # REDIS_TTL_DATA: int | None = None

    @property
    def redis_url(self) -> str:
        if self.REDIS_PASS:
            return f"redis://{self.REDIS_PASS}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"



class Settings(
    NatsBrokerSettings,
    RedisSettings
): ...


settings = Settings()