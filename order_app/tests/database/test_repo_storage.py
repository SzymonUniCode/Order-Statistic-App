from webapp.database.models.storage import Storage
from webapp.database.repositories.storage import StorageRepository
from sqlalchemy.orm import Session
import pytest

def test_storage_get_by_sku(session: Session, storage_repo: StorageRepository, storage: list[Storage]):
    storage_from_db = storage_repo.get_by_sku(storage[0].sku)

    assert storage_from_db is not None
    assert storage_from_db.sku == storage[0].sku



@pytest.mark.parametrize(
    "min_qty, max_qty, expected_len, expected_sku",
    [
        (10, 100, 2, ["SKU-1", "SKU-2"]),
        (11, 100, 1, ["SKU-2"]),
        (10, 1000, 3, ["SKU-1", "SKU-2", "SKU-3"]),
        (101, 103, 0, []),   # poprawione
    ]
)
def test_get_by_qty_between(
    session: Session,
    storage_repo: StorageRepository,
    storage: list[Storage],
    min_qty: int,
    max_qty: int,
    expected_len: int,
    expected_sku: list[str]
):
    result = storage_repo.get_by_qty_between(min_qty, max_qty)

    assert len(result) == expected_len

    result_sort = sorted([r.sku for r in result])
    assert result_sort == expected_sku

def test_get_by_sku_for_update(session: Session, storage_repo: StorageRepository, storage: list[Storage], sku = "SKU-1"):
    result = storage_repo.get_by_sku_for_update(sku)

    assert result is not None
    assert result.sku == sku
    assert result.qty == 10

def test_get_all(session: Session, storage_repo: StorageRepository, storage: list[Storage]):
    result = storage_repo.get_all()

    assert result is not None
    assert len(result) == 3