# Used for Application Factory Pattern. Flask is created dynamically. It creates container of SQLAlchemy but
# it is not know with which app it owrks or database or URI, or engine. It allow to create containrs of needed objects
# for each app which communicate with each other. One big app can handle many micro-services inside - loging, gateway,
# mailing, business service part of app

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
