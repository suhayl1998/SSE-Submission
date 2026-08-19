class AppError(Exception):
    def __init__(
        self,
        detail: str,
        status_code: int = 400,
        title: str = "Application Error",
        type_: str = "about:blank",
        **extra,
    ):
        self.detail = detail
        self.status_code = status_code
        self.title = title
        self.type_ = type_
        self.extra = extra
        super().__init__(detail)