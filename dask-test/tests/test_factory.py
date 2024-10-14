import pytest

from dask_test import factory, models


@pytest.mark.parametrize(("client_type"), [x.name for x in models.ClientType])
def test_create_client(client_type: str) -> None:
    client = factory.create_client(models.ClientType[client_type])
    assert client is not None
