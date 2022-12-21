import allure

from app.api.client.base_api import BaseAPI


class AppAPIClient(BaseAPI):
    """
    App API
    """
    def add_user(self, data=None, method="POST", path="/api/user",
                 expected_status=None, content_type=None, jsonify=False):
        """
        Add new user via POST request. Request example:

            POST http://<APP_HOST>:<APP_PORT>/api/user
            Content-Type: application/json
            Body:
            {
                "name": "<name>",
                "surname": "<surname>",
                "middle_name": "<middle_name>",
                "username": "<username>",
                "password": "<password>",
                "email": "<email>"
            }

        """
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify)

    def change_password(self, data=None, method="PUT", path="/api/user/<username>/change-password",
                        expected_status=None, content_type=None, jsonify=False,
                        username=None, repeat=1):
        """
        Change user password via PUT request. Request example:

            PUT http://<APP_HOST>:<APP_PORT>/api/user/<username>/change-password
            Content-Type: application/json
            Body:
            {
                "password": "<new password>"
            }

        """
        if username is not None:
            path = f"/api/user/{username}/change-password"
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify)

    def delete_user(self, data=None, method="DELETE", path="/api/user/<username>",
                    expected_status=None, content_type=None, jsonify=False):
        """
        Delete user via DELETE request
        """
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify)

    def block_user(self, data=None, method="POST", path="/api/user/<username>/block",
                   expected_status=None, content_type=None, jsonify=False, username=None, repeat=1):
        """
        Block user via POST request
        """
        if username is not None:
            path = f"/api/user/{username}/block"
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify, repeat=repeat)

    def unblock_user(self, data=None, method="POST", path="/api/user/<username>/accept",
                     expected_status=None, content_type=None, jsonify=False,
                     username=None, repeat=1):
        """
        Unblock user via POST request
        """
        if username is not None:
            path = f"/api/user/{username}/accept"
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify, repeat=repeat)

    def get_status(self, method="GET", path="/status", expected_status=None,
                   data=None, content_type=None, jsonify=False):
        """
        Get App status. Response example:

            Status: 200 OK
            Content-Type: application/json
            Body:
            {
                "status": "ok"
            }

        """
        return self._request(method=method, path=path, data=data, content_type=content_type,
                             expected_status=expected_status, jsonify=jsonify)
