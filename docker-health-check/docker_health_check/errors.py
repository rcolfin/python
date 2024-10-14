class NotificationError(RuntimeError):
    pass


class EmailNotificationError(NotificationError):
    pass


class EmailNotSupportedError(EmailNotificationError):
    pass


class ContainerRestartError(RuntimeError):
    pass
