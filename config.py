import os
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set")
        self.SQLALCHEMY_DATABASE_URI = self.get_database_uri()

    def get_database_uri(self):
        raise NotImplementedError("Subclasses must implement get_database_uri")


class DevelopmentConfig(Config):
    DEBUG = True

    def __init__(self):
        # Provide fallback for SECRET_KEY in development
        if not os.getenv("SECRET_KEY"):
            print("WARNING: Using default development SECRET_KEY")
            os.environ["SECRET_KEY"] = "dev-secret-key"
        super().__init__()

    def get_database_uri(self):
        return os.getenv(
            "DEV_DATABASE_URL",
            "mysql+pymysql://root:@localhost/fyp"
        )


class ProductionConfig(Config):
    DEBUG = False

    def get_database_uri(self):
        database_url = os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://sql8784725:t236ViBS52@sql8.freesqldatabase.com:3306/sql8784725"
        )
        if not database_url:
            raise ValueError("DATABASE_URL environment variable must be set in production")

        parsed_url = urlparse(database_url)
        if not parsed_url.scheme.startswith('mysql'):
            raise ValueError("DATABASE_URL must use mysql protocol")

        return database_url


# Select environment configuration
env = os.getenv("FLASK_ENV", "development").lower()
if env not in ["development", "production"]:
    raise ValueError(f"Invalid FLASK_ENV: {env}. Must be 'development' or 'production'")

current_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}[env]()
