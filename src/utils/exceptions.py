from starlette import status


class HouseNotFoundException(Exception):
    def __init__(
        self, detail="House not found", status_code=status.HTTP_404_NOT_FOUND
    ):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)
