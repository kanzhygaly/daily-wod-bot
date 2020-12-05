from typing import NamedTuple


class PageDto(NamedTuple):
    url: str
    login_path: str

    def get_login_url(self) -> str:
        return self.url + self.login_path


class UserDto(NamedTuple):
    login: str
    password: str


class DbCredentials(NamedTuple):
    user: str
    password: str
    host: str
    port: str
    database: str

    @classmethod
    def from_string(cls, url: str):
        arr = url.replace('postgres://', '').replace('@', ' ').replace(':', ' ').replace('/', ' ').split()
        credentials = cls._make(arr)
        return credentials

