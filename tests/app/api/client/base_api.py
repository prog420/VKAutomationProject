import allure
import requests
from urllib.parse import urljoin
from app.api.exceptions import *


class BaseAPI:
    """
    Base functions
    """
    def __init__(self, base_url=None, auth=False, username=None, password=None):
        self.base_url = base_url
        self.session = requests.Session()
        if auth:
            self.auth(username=username, password=password)

    @allure.step("{method} Request to {path}")
    def _request(self, method, path, headers=None, data=None, params=None, content_type=None,
                 allow_redirects=False, expected_status=None, jsonify=False, repeat=1):
        """
        :param method: required HTTP method
        :param path: <protocol>://<domain name>/<path>
        :param headers: required headers for request
        :param data: data for POST requests
        :param params: parameters for GET requests
        :param content_type: content type of request body
        :param allow_redirects: allow redirects if True
        :param expected_status: expected status code of response
        :param jsonify: return response in json format if True
        :param repeat: repeat request and return last response
        :return: request.Response
        """
        response = None
        url = urljoin(self.base_url, path)
        headers = self.session.headers if headers is None else headers
        if content_type:
            headers["Content-Type"] = content_type
        for i in range(repeat):
            response = self.session.request(method=method, url=url, headers=headers, data=data,
                                            params=params, allow_redirects=allow_redirects)
        if expected_status is not None and response.status_code != expected_status:
            reason = f"Expected {expected_status}, got {response.status_code} {response.reason}"
            try:
                reason += f" - {response.json()['detail']}"
            except requests.exceptions.JSONDecodeError:
                ...
            raise ResponseStatusCodeException(reason)
        if jsonify:
            return response.json()
        return response

    def auth(self, path="/login", username=None, password=None):
        headers = {
            "Referer": f"http://{self.base_url}{path}"
        }
        data = {
            "username": username,
            "password": password,
            "submit": "Login"
        }
        r = self._request(
            method="POST", path=path, headers=headers, data=data, jsonify=False
        )
