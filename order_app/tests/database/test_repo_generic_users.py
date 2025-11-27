from webapp.database.models.users import User
from webapp.database.repositories.users import UserRepository
from sqlalchemy.orm import Session


def test_user_crud_add_and_get(session: Session, user_repo: UserRepository, user_1: User):
    user_repo.add(user_1)

    session.flush()

    u = user_repo.get(user_1.id)    # IDE do not handle this. However, it is correct

    assert u is not None
    assert u.username == "John Test 1"


def test_user_crud_add_all_and_get_all(session: Session, user_repo: UserRepository, users: list[User]):
    user_repo.add_all(users)

    session.flush()

    u = user_repo.get_all()

    assert len(u) == 2
    assert u[0].id is not None
    assert u[0].username == "John Test 1"
    assert u[1].id is not None
    assert u[1].username == "John Test 2"

def test_user_crud_delete_and_delete_by_id(session: Session, user_repo: UserRepository, users: list[User]):
    user_repo.add_all(users)
    session.flush()

    user_repo.delete(users[0])

    u_1 = user_repo.get_all()
    assert len(u_1) == 1

    user_repo.delete_by_id(users[1].id)     # IDE do not handle this. However, it is correct

    u_2 = user_repo.get_all()
    assert len(u_2) == 0


def test_user_crud_get_by_username(session: Session, user_repo: UserRepository, user_1: User):
    user_repo.add(user_1)
    session.flush()

    u = user_repo.get_by_username(user_1.username)
    assert u is not None
    assert u.username == user_1.username
