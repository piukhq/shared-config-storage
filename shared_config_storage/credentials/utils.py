import hashlib
import json
from enum import Enum


def generate_lookup_hash(credentials: dict) -> str:
    return hashlib.md5(json.dumps(credentials, sort_keys=True).encode()).hexdigest()


class AnswerTypeChoices(Enum):
    TEXT = 0
    SENSITIVE = 1
    CHOICE = 2
    BOOLEAN = 3
    PAYMENT_CARD_ID = 4
