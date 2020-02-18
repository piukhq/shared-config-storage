import base64
import hashlib
from enum import Enum
from typing import Union, Dict, Iterable

import hvac
import requests
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import BLAKE2s
from Crypto.PublicKey import RSA
from hvac.exceptions import Forbidden


class KeyTypes(str, Enum):
    PUBLIC_KEY = "public_key"
    PRIVATE_KEY = "private_key"
    SALT = "salt"


class AESCipher(object):
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key).digest()

    def encrypt(self, raw):
        if raw == '':
            raise TypeError('Cannot encrypt nothing')
        raw = self._pad(raw.encode('utf-8'))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        if enc == '':
            raise TypeError('Cannot decrypt nothing')
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        length = self.bs - (len(s) % self.bs)
        return s + bytes([length]) * length

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class RSACipher:
    """
    Encrypts/decrypts data using a per-client secret stored in hashicorp vault.
    This should only be used for data within a few hundred bytes in size due
    to RSA limitations.

    RSA is only able to encrypt data to a maximum amount equal to your
    key size (2048 bits = 256 bytes), minus any padding and header data
    (11 bytes for PKCS#1 v1. 5 padding)
    """
    def __init__(self, vault_token: str, vault_url: str, bundle_id: str = None):
        self.pub_key = None
        self.priv_key = None
        self.bundle_id = bundle_id
        self.vault_token = vault_token
        self.vault_url = vault_url

    def encrypt(self, val: Union[str, int, Dict, Iterable]) -> str:
        if not self.pub_key:
            self.pub_key = RSA.import_key(
                self.get_secret_key(self.bundle_id, KeyTypes.PUBLIC_KEY)
            )

        cipher = PKCS1_OAEP.new(self.pub_key)

        # convert all values to string before encoding as some values may be integers
        encrypted_val = cipher.encrypt(str(val).encode())
        # encrypted byte string cannot be sent in JSON so must be converted
        return base64.b64encode(encrypted_val).decode('utf-8')

    def decrypt(self, val: str) -> str:
        try:
            val = base64.b64decode(val.encode())
        except AttributeError as e:
            err_msg = f"Unable to decrypt value. Value must be of type string: {val}"
            raise TypeError(err_msg) from e

        if not self.priv_key:
            self.priv_key = RSA.import_key(
                self.get_secret_key(self.bundle_id, KeyTypes.PRIVATE_KEY)
            )
        cipher = PKCS1_OAEP.new(self.priv_key)

        decrypted_val = cipher.decrypt(val).decode('utf-8')
        return decrypted_val

    def get_secret_key(self, save_path: str, key_name: str) -> str:
        if not save_path or not self.bundle_id:
            raise Exception("Missing bundle_id for retrieving public key")
        elif self.bundle_id and not save_path:
            save_path = self.bundle_id

        client = hvac.Client(token=self.vault_token, url=self.vault_url)
        try:
            val = client.read(f'secret/data/{save_path}')['data']['data'][key_name]
            return val
        except TypeError as e:
            raise ValueError('Could not locate security credentials in vault') from e
        except (requests.RequestException, hvac.exceptions.VaultError) as e:
            raise ConnectionError('Error connecting to vault') from e


class BLAKE2sHash:
    """
    Hashes a string using the BLAKE2s algorithm.

    If a key/salt is provided to .new(), there is no need to provide vault
    details in __init__().

    If a key/salt is not provided then there will be an attempt to locate
    one in Hashicorp vault using the secret_path and key_name.

    :param vault_token: Authorisation token to access Hashicorp Vault
    :param vault_url: URL to access Hashicorp Vault
    :param secret_path: Path in the Vault where the hash secret is stored
    :param key_name: Name of the secret under which it is stored
    """
    def __init__(
            self,
            vault_token: str = None,
            vault_url: str = None,
            secret_path: str = 'pcard_hash_secret',
            key_name: str = 'salt'
    ) -> None:
        self.vault_token = vault_token
        self.vault_url = vault_url
        self.hash_secret = None
        self.secret_path = secret_path
        self.key_name = key_name

    def get_secret_key(self, path: str = None, key_name: str = None) -> str:
        if self.hash_secret:
            return self.hash_secret

        if not path:
            path = self.secret_path

        if not self.vault_url and self.vault_token:
            raise AttributeError("Missing vault token and vault url")

        client = hvac.Client(token=self.vault_token, url=self.vault_url)
        try:
            val = client.read(f'secret/data/{path}')['data']['data'][key_name]
        except TypeError as e:
            raise ValueError('Could not locate security credentials in vault') from e
        except (requests.RequestException, hvac.exceptions.VaultError) as e:
            raise ConnectionError('Error connecting to vault') from e

        self.hash_secret = val
        return val

    def new(self, obj: str, digest_bits: int = 256, key: str = None) -> str:
        if not key:
            try:
                key = self.get_secret_key(self.secret_path, key_name=self.key_name)
            except KeyError as e:
                raise ValueError(f"{self.key_name} not found in vault.") from e

        hash2 = BLAKE2s.new(digest_bits=digest_bits, key=key.encode())
        hash2.update(obj.encode())

        return hash2.hexdigest()
