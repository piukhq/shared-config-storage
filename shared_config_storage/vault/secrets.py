import json
import requests
import logging


class VaultReadError(Exception):
    pass


class VaultChannelSecrets:

    _bundle_secrets = {}

    def __init__(self, url, token, channel_path="/channels", vault_logger=None, vault_exception=VaultReadError):
        """
        On startup retrieves security credential values from channel secrets storage vault.
        The returned record from read vault returns all data for every bundle from which jwt_secret is extracted

        data is passed into _bundle_secrets which is used as a cache for API authentication by bundle

        """
        if vault_logger:
            self.vault_logger = vault_logger
        else:
            self.vault_logger = logging.getLogger('channel_vault')

        self.vault_exception = vault_exception
        self.url = url
        self.token = token
        self.channel_path = channel_path

    def load_secrets(self, local_channel_secrets=False, local_secrets_path="my_secrets.json"):

        if local_channel_secrets:
            self.vault_logger.info(f"Channel bundle secrets - from local file {local_secrets_path}")
            with open(local_secrets_path) as fp:
                self._bundle_secrets = json.load(fp)
        else:
            self.vault_logger.info(f"Channel bundle secrets - from vault at {self.url}  secrets: {self.channel_path}")
            try:
                self._bundle_secrets = read_vault(self.channel_path, self.url, self.token)
            except requests.RequestException as e:
                self.vault_logger.exception(f"Channel bundle secrets - Vault Exception {e}")
                raise self.vault_exception(f'Channel bundle secrets - Exception {e}') from e

        self.vault_logger.info(f"Channel bundle secrets - Found secrets for"
                               f" {[bundle_id for bundle_id in self._bundle_secrets]}")

    def get_jwt_secret(self, bundle_id):
        try:
            return self._bundle_secrets[bundle_id]['jwt_secret']
        except KeyError as e:
            self.vault_logger.error(f"No bundle defined: {e}")
            raise self.vault_exception(f"JWT is invalid: {e}") from e

    def get_pcard_secret(self, bundle_id):
        try:
            return self._bundle_secrets[bundle_id]['pcard']
        except KeyError as e:
            self.vault_logger.error(f"No pcard defined for bundle {bundle_id} exception {e}")
            raise self.vault_exception(f"No pcard defined for bundle {bundle_id} exception {e}") from e


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
