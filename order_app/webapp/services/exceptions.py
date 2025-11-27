class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass


class ValidationException(ServiceException):
    pass


class NotEnoughStockException(ServiceException):
    pass
