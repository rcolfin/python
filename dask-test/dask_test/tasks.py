import os


def echo(message: str) -> str:
    pid = os.getpid()
    return f"{message} from pid: {pid}."
