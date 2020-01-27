import requests


class VaultError(Exception):
    """Exception raised for errors in the input.
    """

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return f"Vault Error: {self.message}"


def read_vault(secret_path, url, token):
    """

    :param secret_path: path within the secrets engine eg  /channels or /data
    :param url: domain and port to access vault by https:
    :param token: access token
    :return:  json data structure of the secret_path eg for /channels would be:
            {
            "com.barclays.test": {
                    "jwt_secret": "THE SECRET DATA"
            },
            "com.bink.daedalus": {
                    "jwt_secret": "THE SECRET DATA"
            }


    """
    headers = {
        "X-Vault-Token": token

    }
    path = f"{url}/v1/secret{secret_path}"
    try:
        response = requests.get(path, headers=headers)
        if response.status_code != 200:
            raise VaultError(f'Error connecting status code {response.status_code}')
    except requests.RequestException as e:
        raise VaultError('Error connecting') from e
    return response.json().get('data', {})
