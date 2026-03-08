from enum import Enum, EnumMeta, StrEnum
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Iterable


class _CaseInsensitiveEnumMeta(EnumMeta):
    def __call__(cls, value: str, *args: Any, **kwargs: Any):  # type: ignore # noqa: ANN401 ANN204 PGH003
        try:
            return super().__call__(value, *args, **kwargs)
        except ValueError:
            items = cast("Iterable[Enum]", cls)
            for item in items:
                if item.name.casefold() == value.casefold():
                    return cast("type[Enum]", item)
            raise


class ContainerStatus(StrEnum, metaclass=_CaseInsensitiveEnumMeta):
    EXITED = "exited"
    PAUSED = "paused"
    RUNNING = "running"
    RESTARTING = "restarting"


class HealthCheck(StrEnum, metaclass=_CaseInsensitiveEnumMeta):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class RestartStatus(StrEnum, metaclass=_CaseInsensitiveEnumMeta):
    SUCCESS = "success"
    FAILURE = "failure"
