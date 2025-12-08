# Place where register services and repos. Repos will be as providers for services. It gatter all repos in one place
# and gives singleton which makes services to use only one instance of each repo instead of creating new instances for
# each service. After that we do the same with services where we put repos to each service. It does not create services
# but inform program where it will be possible and what is goes inside the service.

from dependency_injector import containers, providers
from webapp.database.repositories.orders import TotalOrderRepository
from webapp.database.repositories.products import ProductRepository
from webapp.database.repositories.storage import StorageRepository
from webapp.database.repositories.users import UserRepository

from webapp.services.orders.service import OrderService
from webapp.services.products.service import ProductService
from webapp.services.storage.service import StorageService
from webapp.services.users.service import UserService

class Container(containers.DeclarativeContainer):

    # Ustawia domyslne miejsca, gdzie biblioteka bedzie wstrzykiwac zaleznosci.
    # Dzieki temu w tych miejscach uzyjesz @inject, Provide[...]
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.orders",
            "webapp.api.products",
            "webapp.api.storage",
            "webapp.api.users"
        ]
    )



    # Create containers to inject

    user_repository = providers.Singleton(UserRepository)
    storage_repository = providers.Singleton(StorageRepository)
    products_repository = providers.Singleton(ProductRepository)
    total_orders_repository = providers.Singleton(TotalOrderRepository)


    order_service = providers.Singleton(
        OrderService,
        order_repo = total_orders_repository,
        storage_repo = storage_repository,
        user_repo = user_repository
    )

    product_service = providers.Singleton(
        ProductService,
        product_repo = products_repository
    )


    storage_service = providers.Singleton(
        StorageService,
        storage_repo = storage_repository,
        product_repo = products_repository
    )

    user_service = providers.Singleton(
        UserService,
        user_repo = user_repository
    )
