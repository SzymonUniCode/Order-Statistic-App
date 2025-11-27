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
# C) Fixtures models
# ---------------------------------------------------------
@pytest.fixture
def product_model(session):
    from webapp.database.models.products import Product
    p = Product(sku="SKU-123", name="Product Test 1", price=100.4)
    session.add(p)
    session.flush()
    return p

@pytest.fixture
def user_model(session):
    from webapp.database.models.users import User
    u = User(username="John Test")
    session.add(u)
    session.flush()
    return u

@pytest.fixture
def storage_model(session):
    from webapp.database.models.storage import Storage
    s = Storage(sku="SKU-123", qty=100)
    session.add(s)
    session.flush()
    return s

@pytest.fixture
def order_model(session):
    from webapp.database.models.orders import Order
    o = Order(id=1, user_id=1)
    session.add(o)
    session.flush()
    return o


@pytest.fixture
def order_details_model(session):
    from webapp.database.models.order_details import OrderDetail
    od = OrderDetail(order_id=1, product_sku="SKU-123", qty=50)
    session.add(od)
    session.flush()
    return od



# ---------------------------------------------------------
# D) Fixtures User & Generic Repository
# ---------------------------------------------------------

@pytest.fixture
def user_repo():
    from webapp.database.repositories.users import UserRepository
    return UserRepository()


@pytest.fixture
def user_1(session):
    from webapp.database.models.users import User
    u_1 = User(username="John Test 1")
    return u_1

@pytest.fixture
def user_2(session):
    from webapp.database.models.users import User
    u_2 = User(username="John Test 2")
    return u_2


@pytest.fixture
def users(user_1, user_2):
    return [user_1, user_2]


# ---------------------------------------------------------
# E) Fixtures Product Repository
# ---------------------------------------------------------

@pytest.fixture
def product_repo():
    from webapp.database.repositories.products import ProductRepository
    return ProductRepository()


@pytest.fixture
def product_1(session):
    from webapp.database.models.products import Product
    p_1 = Product(sku="SKU-1", name="Product Test 1", price=10.1)
    return p_1

@pytest.fixture
def product_2(session):
    from webapp.database.models.products import Product
    p_2 = Product(sku="SKU-2", name="Product Test 2", price=100.9)
    return p_2

@pytest.fixture
def product_3(session):
    from webapp.database.models.products import Product
    p_3 = Product(sku="SKU-3", name="Product Test 3", price=1000.4)
    return p_3


@pytest.fixture
def products(session, product_1, product_2, product_3):
    session.add_all([product_1, product_2, product_3])
    session.flush()
    return [product_1, product_2, product_3]


# ---------------------------------------------------------
# F) Fixtures Storage Repository
# ---------------------------------------------------------

@pytest.fixture
def storage_repo():
    from webapp.database.repositories.storage import StorageRepository
    return StorageRepository()

@pytest.fixture
def storage(session):
    from webapp.database.models.storage import Storage
    stores =[
            Storage(sku="SKU-1", qty=10),
            Storage(sku="SKU-2", qty=100),
            Storage(sku="SKU-3", qty=1000)
        ]

    session.add_all(stores)
    session.flush()

    return stores


# ---------------------------------------------------------
# G) Fixtures Orders Repository
# ---------------------------------------------------------

@pytest.fixture
def order_repo():
    from webapp.database.repositories.orders import TotalOrderRepository
    return TotalOrderRepository()


@pytest.fixture
def orders(session):
    from webapp.database.models.orders import Order
    from webapp.database.models.order_details import OrderDetail
    from webapp.database.models.products import Product

    products = [
        Product(sku="SKU-1", name="P1", price=10.0),
        Product(sku="SKU-2", name="P2", price=20.0),
        Product(sku="SKU-3", name="P3", price=30.0),
    ]
    session.add_all(products)
    session.flush()

    order_1 = Order(user_id=1)
    order_1.order_details.append(OrderDetail(product_sku="SKU-1", qty=10))
    order_1.order_details.append(OrderDetail(product_sku="SKU-2", qty=20))


    order_2 = Order(user_id=2)
    order_2.order_details.append(OrderDetail(product_sku="SKU-3", qty=30))

    order_3 = Order(user_id=1)

    session.add_all([order_1, order_2, order_3])
    session.flush()

    return [order_1, order_2, order_3]
