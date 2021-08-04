import pytest
import random
import string

from shared_config_storage.credentials import encryption


def random_string(n: int) -> str:
    return ''.join(random.choices(string.printable, k=n))


@pytest.mark.parametrize("key_length,data_length", [
    (5, 20),
    (12, 42),
    (26, 7),
    (42, 42)
])
def test_aes_encryption_decryption(key_length, data_length):
    key = random_string(key_length).encode()
    data = random_string(data_length)

    aes = encryption.AESCipher(key)

    ciphertext = aes.encrypt(data)
    assert ciphertext != data

    plaintext = aes.decrypt(ciphertext)
    assert plaintext == data


def test_aes_encryption_decryption_no_data():
    aes = encryption.AESCipher(b'test')

    with pytest.raises(TypeError):
        aes.encrypt("")

    with pytest.raises(TypeError):
        aes.decrypt("")


def test_rsa_encryption_decryption(vault, key_pair):
    vault.add_secret("some_keys", json_data={"data": key_pair}, status=200)

    rsa = encryption.RSACipher(vault_token="test", vault_url=vault.url, keys_path="some_keys")

    original = "some secret data"
    ciphertext = rsa.encrypt(original)
    assert ciphertext != original

    plaintext = rsa.decrypt(ciphertext)
    assert plaintext == original


@pytest.mark.parametrize("key,digest_bits,data,expected", [
    ("testkey1234", 256, "somedata", "db0a2f4f2a509c07722486b0f9685a2ca8350fbde5853fb1200d8b7cbd12f521"),
    ("somekey", 128, "somedata2", "f0b8cfe4a72fea368af7cb9805488b12"),
    ("lol", 64, "somedata3", "dd63790467eecf2b"),
])
def test_blake2_hashes(key, digest_bits, data, expected):
    blake2 = encryption.BLAKE2sHash()
    hash_value = blake2.new(data, digest_bits, key)
    assert hash_value == expected


def test_blake2_hash_vault_salt(vault, blake_salt):
    vault.add_secret("data/some_keys", json_data={"data": blake_salt}, status=200)

    blake2 = encryption.BLAKE2sHash(vault_token="test", vault_url=vault.url, secret_path="some_keys")

    data = "test"
    hash_value = blake2.new(data, 256)
    assert hash_value == "c8a80a86f1bd0a932311a950a215ef243a9c1deb2d7c29608108525b30ca7c76"
