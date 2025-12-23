from typing import Any, Generator

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from sqlalchemy.pool import StaticPool

from webapp.database.models.users import User
from webapp.extensions import db
from webapp.container import Container


@pytest.fixture(autouse=True)
def app() -> Generator[Flask, Any, None]:
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        },
    )

    db.init_app(app)

    container = Container()
    container.wire(
        packages=[
            "webapp.api.users",
            "webapp.api.products",
            "webapp.api.storage",
            "webapp.api.orders",
        ]
    )

    from webapp.api import api_bp
    app.register_blueprint(api_bp)

    @app.after_request
    def cleanup(response: Response) -> Response:
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
        finally:
            db.session.remove()
        return response


    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
        db.session.remove()
        db.engine.dispose()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()



@pytest.fixture()
def seed_user_data(app: Flask) -> None:
    with app.app_context():
        user_1 = User(username="John Test 1")
        user_2 = User(username="John Test 2")
        db.session.add_all([user_1, user_2])
        db.session.commit()


