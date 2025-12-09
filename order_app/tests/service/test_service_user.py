from unittest.mock import MagicMock, patch
import pytest

from tests.service.conftest import fake_user_with_orders
from webapp.database.models.users import User
from webapp.database.repositories.users import UserRepository
from webapp.services.users.service import UserService
from webapp.services.users.dtos import CreateUserDTO, ReadUserDTO
from webapp.services.exceptions import NotFoundException, UserAlreadyExistsException


@patch("webapp.services.users.service.db")                                  # do not allow open real db connection
def test_get_all(mock_db: MagicMock, mock_user_service: UserService, mock_user_repo: UserRepository, fake_user_with_orders):

    mock_user_repo.get_all.return_value = [fake_user_with_orders]           # set the return for get_all method

    result = mock_user_service.get_all()

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].name == "John Test 1"
    assert result[0].orders_qty == 3



@patch("webapp.services.users.service.db")
def test_get_by_username(mock_db: MagicMock, mock_user_service: UserService, mock_user_repo: UserRepository, fake_user_with_orders):

    mock_user_repo.get_by_username.return_value = fake_user_with_orders

    result = mock_user_service.get_by_username("John Test 1")

    assert result.id == 1
    assert result.name == "John Test 1"
    assert result.orders_qty == 3





@patch("webapp.services.users.service.db")
def test_delete_user_by_id_success(mock_db, mock_user_service, mock_user_repo, fake_user_with_orders):

    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_user_repo.get.return_value = fake_user_with_orders

    result = mock_user_service.delete_user_by_id(1)

    mock_user_repo.delete.assert_called_once_with(fake_user_with_orders)
    assert result == "User with id 1 deleted successfully."



@patch("webapp.services.users.service.db")
def test_delete_user_by_id_error(mock_db, mock_user_service, mock_user_repo, fake_user_with_orders):

    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_user_repo.get.return_value = None

    with pytest.raises(NotFoundException):
        mock_user_service.delete_user_by_id(1)



@patch("webapp.services.users.service.db")
def test_delete_user(mock_db, mock_user_service, mock_user_repo, fake_user_with_orders):

    mock_db.session.begin.return_value.__enter__.return_value = None

    mock_user_repo.get.return_value = fake_user_with_orders

    result = mock_user_service.delete_user(fake_user_with_orders)


    mock_user_repo.delete.assert_called_once_with(fake_user_with_orders)
    assert result == "User John Test 1 deleted successfully."


@patch("webapp.services.users.service.db")
def test_add_user_success(mock_db, mock_user_service, mock_user_repo):

    mock_db.session.begin.return_value.__enter__.return_value = None

    dto = CreateUserDTO(name="John Test 1")

    fake_user = User(username="John Test 1")

    mock_user_repo.get_by_username.return_value = None
    mock_user_repo.add.return_value = fake_user

    result = mock_user_service.add_user(dto)

    # do not check id in asserting because this test does not have a flush, due to not using real db

    mock_user_repo.add.assert_called_once()
    assert result.name == "John Test 1"


@patch("webapp.services.users.service.db")
def test_add_user_error(mock_db, mock_user_service, mock_user_repo):

    mock_db.session.begin.return_value.__enter__.return_value = None
    mock_user_repo.get_by_username.return_value = MagicMock()

    with pytest.raises(UserAlreadyExistsException):
        mock_user_service.add_user(CreateUserDTO(name="John Test 1"))

