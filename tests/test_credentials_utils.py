import pytest
from shared_config_storage.credentials import utils


@pytest.mark.parametrize("credentials,expected_hash", [
    ({"a": 1, "b": 1}, "386b19932c82f3f9749dd6611e846293"),
    ({"b": 1, "a": 1}, "386b19932c82f3f9749dd6611e846293"),
    ({"b": 1}, "d58e48889e29ab6a963ac6ade67f431e"),
])
def test_lookup_hash_generation(credentials, expected_hash):
    hash_value = utils.generate_lookup_hash(credentials)
    assert hash_value == expected_hash
