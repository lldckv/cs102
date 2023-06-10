import typing as tp

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.session = requests.Session()
        retry = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=[500, 400])
        adapter = HTTPAdapter(max_retries=retry)
        self.base_url = base_url.rstrip("/")
        self.session.mount(self.base_url, adapter)
        self.session.headers.update({"Content-Type": "application/json"})
        self.timeout = timeout

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        full_url = self.base_url + url
        try:
            return self.session.get(full_url, *args, **kwargs)
        except requests.exceptions.RetryError:
            raise requests.exceptions.RetryError()

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        full_url = self.base_url + url
        try:
            return self.session.post(full_url, *args, **kwargs)
        except requests.exceptions.RetryError:
            raise requests.exceptions.RetryError()
