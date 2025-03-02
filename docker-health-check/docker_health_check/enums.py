from enum import Enum, EnumMeta
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from collections.abc import Iterable


class _CaseInsensitiveEnumMeta(EnumMeta):
    def __call__(cls, value: str, *args: list[Any], **kwargs: Any) -> type[Enum]:  # noqa: ANN401
        try:
            return super().__call__(value, *args, **kwargs)
        except ValueError:
            items = cast("Iterable[Enum]", cls)
            for item in items:
                if item.name.casefold() == value.casefold():
                    return cast("type[Enum]", item)
            raise


class ContainerStatus(str, Enum, metaclass=_CaseInsensitiveEnumMeta):
    EXITED = "exited"
    PAUSED = "paused"
    RUNNING = "running"
    RESTARTING = "restarting"


class HealthCheck(str, Enum, metaclass=_CaseInsensitiveEnumMeta):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"


class RestartStatus(str, Enum, metaclass=_CaseInsensitiveEnumMeta):
    SUCCESS = "success"
    FAILURE = "failure"
