from dask.distributed import Client, LocalCluster

from dask_test import models


def create_process_client() -> Client:
    cluster = LocalCluster()
    return cluster.get_client()


def create_thread_client() -> Client:
    return Client(threads_per_worker=4, n_workers=1)


def create_client(client: models.ClientType) -> Client:
    if client == models.ClientType.THREAD:
        return create_thread_client()

    if client == models.ClientType.PROCESS:
        return create_process_client()

    error = f"{client} is not supported."
    raise NotImplementedError(error)
