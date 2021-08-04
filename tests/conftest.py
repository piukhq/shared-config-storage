import string

import pytest
import random
from typing import Dict, Any
from pytest_httpserver import HTTPServer


class Vault:
    def __init__(self, httpserver: HTTPServer):
        self.httpserver = httpserver

    def add_secret(self, secret_path: str, json_data: Dict[str, Any], status: int = 200) -> None:
        secret_path = secret_path.removeprefix("/")
        self.httpserver.expect_request(f"/v1/secret/{secret_path}").respond_with_json(json_data, status=status)

    @property
    def url(self) -> str:
        return self.httpserver.url_for("").removesuffix("/")


@pytest.fixture
def vault(httpserver: HTTPServer) -> Vault:
    return Vault(httpserver)


TEST_PUBLIC_KEY = (
    "-----BEGIN RSA PUBLIC KEY-----\n"
    "MIIBCgKCAQEAsw2VXAHRqPaCDVYI6Lug3Uq9Quik7m3sI8BkzqdCkBmakPZ5cssb\n"
    "c4EsxETTA9V0V1KDMUy6vGUSaN8pbg4MPDZOzUlJyOcBAhaKWpUH4Bw0OlBtKPVe\n"
    "wN51n8NZHvwqh39f5rwVNVB5T2haTOsuG0Q7roH5TPYs75F87bELwRLCnWyXo69f\n"
    "6o6fH7N+M2CN11S1UKT7ZkqaL2fm3LWuf8GWAkOrvrZp6js3kKCCuztI+JxP93Aa\n"
    "3411aVH1jt0Wgyex+ekdAO2ykGq2tbs9vGi//6ZweZey+B1+2LrCum1+Wulaf1lG\n"
    "LNF5Bo6fHuXXw63fhx54PQe8pMWc5LW93wIDAQAB\n"
    "-----END RSA PUBLIC KEY-----\n"
)


# matching private key for the public key we use in the tests
TEST_PRIVATE_KEY = (
    "-----BEGIN RSA PRIVATE KEY-----\n"
    "MIIEpAIBAAKCAQEAsw2VXAHRqPaCDVYI6Lug3Uq9Quik7m3sI8BkzqdCkBmakPZ5\n"
    "cssbc4EsxETTA9V0V1KDMUy6vGUSaN8pbg4MPDZOzUlJyOcBAhaKWpUH4Bw0OlBt\n"
    "KPVewN51n8NZHvwqh39f5rwVNVB5T2haTOsuG0Q7roH5TPYs75F87bELwRLCnWyX\n"
    "o69f6o6fH7N+M2CN11S1UKT7ZkqaL2fm3LWuf8GWAkOrvrZp6js3kKCCuztI+JxP\n"
    "93Aa3411aVH1jt0Wgyex+ekdAO2ykGq2tbs9vGi//6ZweZey+B1+2LrCum1+Wula\n"
    "f1lGLNF5Bo6fHuXXw63fhx54PQe8pMWc5LW93wIDAQABAoIBAQCEdnQc0SuueE/W\n"
    "VePZaZWkoPpLWZlK2v9ro5XwXEUeHhL/U5idmC0C0nmv6crCd1POljiAbGdpoMxx\n"
    "0UbxKGtc0ECUFrgDbQKN7OcGBGMDJVpuGbnoJz6mKO2T+A0ioyNDgrQMGvEFtDdK\n"
    "y8SiSwqdGWmdvIIWsbiks1lc7zHm7yAUWSp/XYgsw73+xsU+3wRlrEGsUoiTlb5J\n"
    "ZAGXBd95Gix7FQeX04WDP47xtdaydz2G/dhqsN8w78peMDPMNd/LPKMpAHYCT/5b\n"
    "wri0nfzVjNMHULCZU4KoopO8De0M1aik5GwWOdnFx6z/VkW/drXltfc9MKOJKXP7\n"
    "WI5wSCHhAoGBAOmt8z7y5RYuhIum8+e1hsQPb0ah55xcGSK8Vb066xx1XFxlgWB+\n"
    "Xiv+Ga7nQvJm3johLPuIFp0eQKrJ3a+KH+L6biM20S7K5hfxi3qdrHOBd8qKoRWS\n"
    "cbR1V40TYxXTvWYYUa2jnKPsB0msm+3l0jwNLZhygbhwDtw1cNhed2ebAoGBAMQn\n"
    "4UPHU1HE7nUI09eY11eUURuB69TRIoZNO3VVII83RHro7qHyKWk0W2RevjrE8ir2\n"
    "S4ivFYQU5lca6QmcsPj7iGtFbeVImuTWwDTaahCFcfV/pV0L6xxU/7TowKivABHe\n"
    "SUVwZJU+sPPcSSHZRa1uP7/6XD5oZEnysm1Vx6ENAoGBAKQiw/XWRKVE/WLeXPnH\n"
    "Hqb+NGoHdRj1883bPdoR1W0C3mIkBjER8fGypLWeyP5c1QE9pkvzNfccdc3Axw7y\n"
    "1RzoTI49hcb5S49L4W257JShPtQsdaMiXu2jcmCsWm/Nb36T3GM7xd25/xB3xnre\n"
    "b8Iwe3NWEtnLFBUHEIFaMUK7AoGAHoqHDGKQmn6rEhXZxgvKG5zANCQ6b9xQH9EO\n"
    "nOowM5xLUUfLP/PQdszsHeiSfdwESKQohpOcKgCHDLDn79MxytJ/HxSkU7rGQzMc\n"
    "oh4PvZrJb4v8V0xvwu2JEsXamWkF/cI6blFdl883BgEacea+bo5n5qA4lI70bn8X\n"
    "QObGOlECgYAURWOAKLd7RzgNrBorqof4ZZxdNXgOGq9jb4FE+bWI48EvTVGBmt7u\n"
    "9pHA57UX0Nf1UQ/i3dKAvm5GICDUuWHvUnnb3m+pbx0w91YSXR9t8TVNdJ2dMhNu\n"
    "ZSEUFQWbkQLUGtorzjqGssXHxKVa+9riPpztJNDl+8oHhu28wu4WyQ==\n"
    "-----END RSA PRIVATE KEY-----\n"
)


@pytest.fixture(scope='session')
def key_pair():
    return {
        "data": {
            "public_key": TEST_PUBLIC_KEY,
            "private_key": TEST_PRIVATE_KEY
        }
    }


@pytest.fixture(scope='session')
def blake_salt():
    return {
        "data": {
            "salt": 'dd63790467eecf2b'
        }
    }