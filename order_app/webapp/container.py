# Place where register services and repos. Repos will be as providers for services. It gatter all repos in one place
# and gives singleton which makes services to use only one instance of each repo instead of creating new instances for
# each service. After that we do the same with services where we put repos to each service. It does not create services
# but inform program where it will be possible and what is goes inside the service.

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):

    # Ustawia domyslne miejsca, gdzie biblioteka bedzie wstrzykiwac zaleznosci.
    # Dzieki temu w tych miejscach uzyjesz @inject, Provide[...]
    wiring_config = containers.WiringConfiguration(
        packages=[
            "webapp.api.inbound",
            "webapp.api.outbound",
            "webapp.api.storage"
        ]
    )



# Create containers to inject

    # inbound_repository = providers.Singleton(InboundRepository)
    # outbound_repository = providers.Singleton(OutboundRepository)
    # storage_repository = providers.Singleton(StorageRepository)
    #
    #
    # inbound_service = providers.Singleton(
    #     InboundService,
    #     inbound_repository=inbound_repository)
    #
    # outbound_service = providers.Singleton(
    #     OutobundService,
    #     outbound_repository=outbound_repository)
    #
    # storage_service = providers.Singleton(
    #     StorageService,
    #     storage_repository=storage_repository)