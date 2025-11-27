from typing import Generator, TYPE_CHECKING
import pytest                                   # to create fixtures
from flask import Flask                         # create app for tests
from sqlalchemy import StaticPool

if TYPE_CHECKING:
    from webapp.database.models.users import User
    from webapp.database.models.storage import Storage
    from webapp.database.models.products import Product
    from webapp.database.models.orders import Order
    from webapp.database.models.order_details import OrderDetail

from webapp import create_app
from webapp.extensions import db


# ---------------------------------------------------------
# A) Główny fixture — aplikacja + baza in-memory
# ---------------------------------------------------------

@pytest.fixture(scope="package")            # package - once for the whole test's paket
def app() -> Generator[Flask, None, None]:
    application = Flask(__name__)
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        # SQLite-specific engine config
        SQLALCHEMY_ENGINE_OPTIONS={
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    )

    db.init_app(application)

    with application.app_context():
        from webapp.database.models.users import User as _User
        from webapp.database.models.storage import Storage as _Storage
        from webapp.database.models.products import Product as _Product
        from webapp.database.models.orders import Order as _Order
        from webapp.database.models.order_details import OrderDetail as _OrderDetail

        db.create_all()
        yield application
        db.drop_all()
        db.engine.dispose()



# ---------------------------------------------------------
# B) Fixture session → utrzymuje sesję/transakcję dla testu
# ---------------------------------------------------------
@pytest.fixture
def session(app):
    with app.app_context():
        db.session.begin()
        yield db.session
        db.session.rollback()
        db.session.close()


# ---------------------------------------------------------
# C) Fixture product — korzysta z session
# ---------------------------------------------------------
@pytest.fixture
def product(session):
    from webapp.database.models.products import Product
    p = Product(sku="SKU-123", name="Product Test 1", price=100.4)
    session.add(p)
    session.commit()
    return p

@pytest.fixture
def user(session):
    from webapp.database.models.users import User
    u = User(username="John Test")
    session.add(u)
    session.commit()
    return u

@pytest.fixture
def storage(session):
    from webapp.database.models.storage import Storage
    s = Storage(sku="SKU-123", qty=100)
    session.add(s)
    session.commit()
    return s

@pytest.fixture
def order(session):
    from webapp.database.models.orders import Order
    o = Order(id=1, user_id=1)
    session.add(o)
    session.commit()
    return o


@pytest.fixture
def order_details_1(session):
    from webapp.database.models.order_details import OrderDetail
    od_1 = OrderDetail(order_id=1, product_sku="SKU-123", qty=50)
    session.add(od_1)
    session.commit()
    return od_1
