from flask import Flask
from .settings import config
from .container import Container
from .extensions import db, migrate
from .core.error_handlers import register_error_handlers

def create_app() -> Flask:
    app = Flask(__name__)                               # screate flask app engine


    container = Container()                             # create containers of objects to avoid circular dependencies
    container.wire()                                    # check all injections and inject objects to app

    app.config.from_object(config['default'])           # taking settings from whole settings.py and copy them
    config['default'].init_app(app)                     # set copied settings to app.config

    register_error_handlers(app)
    # app.register_blueprint(api_bp)

    from .database.models import users

    db.init_app(app)                                    # connect db to app, without it SQLAlchemy won't work
    migrate.init_app(app, db)                           # connect Migrate to app. We inform Migrate that this is my app and this is my db


    with app.app_context():                             # inform flask that we are inside the app and can use all functionality
        # app.logger.info("[ API GATEWAY ROUTES ]:")    # separator - shown in console line before log below
        # app.logger.info(app.url_map)                  # list of all API's endpoints - allows seeing if all endpoints are working,
                                                        # Dependency injection works if there are no duplicates in endpoints,
                                                        # check if endpoints work before the API starts, better debug-ing
        routes = []

        for rule in app.url_map.iter_rules():
            methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
            routes.append(f"{methods:10}  {rule.rule}")

        app.logger.info("====== API ROUTES ======")
        for r in routes:
            app.logger.info(r)
        app.logger.info("========================")

    return app