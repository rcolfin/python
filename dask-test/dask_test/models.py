from enum import IntEnum, unique


@unique
class ClientType(IntEnum):
    THREAD = 0
    PROCESS = 1
