from decimal import Decimal
from typing import Any, Generator

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from sqlalchemy.pool import StaticPool

from webapp import register_error_handlers
from webapp.database.models.order_details import OrderDetail
from webapp.database.models.orders import Order
from webapp.database.models.products import Product
from webapp.database.models.storage import Storage
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

    register_error_handlers(app)

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


@pytest.fixture()
def seed_product_data(app: Flask) -> None:
    with app.app_context():
        product_1 = Product(sku="SKU-1", name="Test 1", price=Decimal(10.0))
        product_2 = Product(sku="SKU-2", name="Test 2", price=Decimal(20.0))
        product_4 = Product(sku="SKU-4", name="Test 4", price=Decimal(40.0))
        db.session.add_all([product_1, product_2, product_4])
        db.session.commit()


@pytest.fixture()
def seed_storage_data(app: Flask) -> None:
    with app.app_context():
        storage_1 = Storage(sku="SKU-1", qty=10)
        storage_2 = Storage(sku="SKU-2", qty=20)
        db.session.add_all([storage_1, storage_2])
        db.session.commit()


@pytest.fixture()
def seed_order_data(
    app: Flask,
    seed_user_data,
    seed_product_data,
    seed_storage_data
) -> None:
    with app.app_context():

        # Order 1
        order_1 = Order(user_id=1)
        db.session.add(order_1)
        db.session.flush()  # ⬅️ TERAZ order_1.id ISTNIEJE

        order_1.order_details.append(
            OrderDetail(product_sku="SKU-1", qty=10)
        )
        order_1.order_details.append(
            OrderDetail(product_sku="SKU-2", qty=20)
        )

        # Order 2
        order_2 = Order(user_id=2)
        db.session.add(order_2)
        db.session.flush()

        order_2.order_details.append(
            OrderDetail(product_sku="SKU-3", qty=30)
        )

        db.session.commit()

