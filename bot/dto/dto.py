from typing import NamedTuple


class PageDto(NamedTuple):
    url: str
    login_path: str

    def get_login_url(self) -> str:
        return self.url + self.login_path


class UserDto(NamedTuple):
    login: str
    password: str
