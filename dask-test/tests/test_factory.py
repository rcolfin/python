import pytest

from dask_test import factory, types


@pytest.mark.parametrize(("client_type"), [x.name for x in types.ClientType])
def test_create_client(client_type: str) -> None:
    client = factory.create_client(types.ClientType[client_type])
    assert client is not None
