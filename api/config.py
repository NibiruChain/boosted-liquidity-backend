import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@db:5432/yourdb"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = False
    AUTH_TOKEN = os.getenv("AUTH_TOKEN", "mysecrettoken")


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = True
    AUTH_TOKEN = os.getenv("TEST_AUTH_TOKEN", "testsecrettoken")  # Token for tests
