import pytest

from shared_config_storage.vault import secrets


def test_read_vault_bad_status(vault):
    vault.add_secret("data", json_data={}, status=404)

    with pytest.raises(secrets.VaultError):
        secrets.read_vault("/data", vault.url, "sometoken")


def test_read_vault_timeout():
    with pytest.raises(secrets.VaultError):
        secrets.read_vault("/data", "http://0.0.0.0/", "sometoken")


def test_read_vault(vault):
    secret_data = {"blah": 1}
    vault.add_secret("data", json_data={"data": secret_data}, status=200)

    secret = secrets.read_vault("/data", vault.url, "sometoken")
    assert secret == secret_data
