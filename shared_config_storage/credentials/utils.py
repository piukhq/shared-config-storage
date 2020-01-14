import hashlib

from enum import Enum


def hash_credential(credential: str) -> str:
    return hashlib.md5(credential.encode()).hexdigest()


class AnswerTypeChoices(Enum):
    TEXT = 0
    SENSITIVE = 1
    CHOICE = 2
    BOOLEAN = 3
    PAYMENT_CARD_ID = 4
