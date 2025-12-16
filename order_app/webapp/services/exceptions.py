class ServiceException(Exception):
    status_code = 400


class NotFoundException(ServiceException):
    status_code = 404


class ValidationException(ServiceException):
    status_code = 400


class NotEnoughStockException(ServiceException):
    status_code = 409

class ProductAlreadyExistsException(ServiceException):
    status_code = 409

class UserAlreadyExistsException(ServiceException):
    status_code = 409