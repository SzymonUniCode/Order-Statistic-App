from logging.config import dictConfig           # formating logs by dict
from dotenv import load_dotenv                  # divide config from code
from flask import Flask                         # import classes Flask - app's core
from urllib.parse import quote_plus             # code special signs to be safe (space -> +, special sign -> %XX).
                                                # Used because passwords often contain special signs for safety
import os                                       # allow reading ENV + creating log folders


load_dotenv()                                  # allow getting data from .env by writing, for example, os.getenv("MYSQL_USER")


class Config:
    # ------------------------------------------------------------------------------------
    # Basic Flask configuration
    # ------------------------------------------------------------------------------------
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG: bool = os.getenv("FLASK_DEBUG", "False") in ("1", "true", "True")
    TESTING: bool = False

    # ------------------------------------------------------------------------------------
    # Basic MySQL Configuration created by Docker
    # ------------------------------------------------------------------------------------
    MYSQL_DIALECT: str = os.getenv("MYSQL_DIALECT", "mysql+mysqldb")
    MYSQL_HOST: str = os.getenv("DB_HOST", "mysql")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "magazyn")
    MYSQL_USER: str = os.getenv("MYSQL_USER", "user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3308")

    # ------------------------------------------------------------------------------------
    # SQLAlchemy Database URI &
    # ------------------------------------------------------------------------------------
    @property #used to create connection string dynamically - always fresh data from .env config.SQLALCHEMY_DATABASE_URI
    def SQLALCHEMY_DATABASE_URI(self) -> str: # create string connection to database using given data from .env
        return (
            f"{self.MYSQL_DIALECT}://{self.MYSQL_USER}:{quote_plus(self.MYSQL_PASSWORD)}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False # 99% does not need this. It monitors changes in database models

    SQLALCHEMY_ENGINE_OPTIONS: dict[str, bool | int] = {
        "pool_pre_ping": True,              # check connection before using it
        "pool_recycle": 1800,               # close and open a new connection each 30 minutes
        "pool_size": 10,                    # give max 10 requests to database at the same time
        "max_overflow": 20,                 # if all pool_size connections are busy, create 20 new connections in case of overflow
    }

    # ------------------------------------------------------------------------------------
    # Logging - set logs for FLASK and set their format, place of showing logs
    # ------------------------------------------------------------------------------------
    @staticmethod
    def configure_logging(app: Flask) -> None:
        if getattr(app, "_logging_configured", False): # if logs are set, do nothing
            return

        app._logging_configured = True                 # set logs as set. Allow avoiding set logs multiple times
        os.makedirs("logs", exist_ok=True)       # create folder for logs
        logger_level = "DEBUG" if app.config.get("FLASK_DEBUG") else "INFO"     # set level of logs from .env
                                                                                # If true logs are in DEBUG mode which means
                                                                                # logs are detailes. Otherhise, logs are basic for developer

        dictConfig({
            "version": 1,
            "formatters": {
                "default": {
                    "format": (
                        '{"timestamp":"%(asctime)s",'
                        '"level":"%(levelname)s",'
                        '"module":"%(module)s",'
                        '"file":"%(filename)s",'
                        '"line":%(lineno)d,'
                        '"function":"%(funcName)s",'
                        '"pid":%(process)d,'
                        '"message":"%(message)s"}'
                    )
                }
            },
            "handlers": { # show logs in console and in file
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": logger_level,
                },
                "file": { # settings about file, size, howmany backups and level of information
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/app.log",
                    "maxBytes": 5_000_000,
                    "backupCount": 2,
                    "formatter": "default",
                    "level": "DEBUG",
                },
            },
            "root": { # global loger for all places where loggers are not set
                "level": logger_level,
                "handlers": ["console", "file"], # where logs are shown, it can be added also external log system
            },
        })

    # ------------------------------------------------------------------------------------
    # INTEGRATION CONFIGURATION WITH APP OBJECT, SET LOGGERS, SET SQLALCHEMY  ACCORDING FLASK FACTORY FORMAT
    # ------------------------------------------------------------------------------------
    @classmethod
    def init_app(cls, app: Flask) -> None:
        """
        Inject conf from class Config to an app object (Flask app) which is used in create_app() instead of build config again
        """
        cls.configure_logging(app)  # set logs for flask app by function configure_logging

        conf = cls()                # create a config object from class Config to get access to properties

        app.config["SQLALCHEMY_DATABASE_URI"] = conf.SQLALCHEMY_DATABASE_URI                # URI for database
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cls.SQLALCHEMY_TRACK_MODIFICATIONS   # turn off tracking modifications of SQLAlchemy
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = cls.SQLALCHEMY_ENGINE_OPTIONS             # set parameters of the connection pool

        app.logger.debug("Logger initialized")          # inform if logs are set correctly. Visible in DEBUG leve. Test if logs work


# Different configs for different needs. For general purpose default gives Config, if you want to change something, like
# database or logs level for production, I can create a new class ProductionConfig which inherits form Config and
# change database and logs lever and add to this dict.

config: dict[str, type[Config]] = {
    'default': Config,
}