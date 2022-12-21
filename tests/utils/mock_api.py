import requests


class MockAPIClient:
    """
    API Client for Mock server
    """
    def __init__(self, host: str = "localhost", port: str = "8083"):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    def get_all_users(self):
        """
        Check all saved users.
        """
        return requests.get(
            url=f"{self.base_url}"
        )

    def add_user(self, username, vk_id):
        """
        Add new user with VK ID.
        """
        return requests.post(
            url=f"{self.base_url}/user",
            json={"user": username, "vk_id": vk_id}
        )

    def delete_user(self, username):
        """
        Delete specified user.
        """
        return requests.delete(
            url=f"{self.base_url}/user/{username}",
        )

    def get_vk_id(self, username):
        """
        Get VK ID of a user.
        """
        return requests.get(
            url=f"{self.base_url}/vk_id/{username}"
        )

    def change_vk_id(self, username, new_vk_id):
        """
        Change VK ID of a user.
        """
        return requests.put(
            url=f"{self.base_url}/user/{username}/change-vk-id",
            json={"vk_id": new_vk_id}
        )
