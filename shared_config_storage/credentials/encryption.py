import base64
import hashlib
from enum import Enum
from typing import Union, Dict, Iterable

import hvac
import requests
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_OAEP
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
            self.pub_key = RSA.import_key(self.get_secret_key(self.bundle_id, KeyTypes.PUBLIC_KEY))

        cipher = PKCS1_OAEP.new(self.pub_key)

        # convert all values to string before encoding as some values may be integers
        encrypted_val = cipher.encrypt(str(val).encode())
        # encrypted byte string cannot be sent in JSON so must be converted
        return base64.b64encode(encrypted_val).decode('utf-8')

    def decrypt(self, val: str) -> str:
        try:
            val = base64.b64decode(val.encode())
        except AttributeError as e:
            raise TypeError(
                f"Unable to decrypt value. Value must be of type string: {val}") from e

        if not self.priv_key:
            self.priv_key = RSA.import_key(self.get_secret_key(self.bundle_id, KeyTypes.PRIVATE_KEY))
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
