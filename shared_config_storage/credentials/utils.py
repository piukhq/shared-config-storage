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


class EncryptedCredentials(Enum):
    PASSWORD = 'password'
    POSTCODE = 'postcode'
    MEMORABLE_DATE = 'memorable_date'
    PLACE_OF_BIRTH = 'place_of_birth'
    PIN = 'pin'
    TITLE = 'title'
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    FAVOURITE_PLACE = 'favourite_place'
    DATE_OF_BIRTH = 'date_of_birth'
    PHONE = 'phone'
    PHONE_2 = 'phone_2'
    GENDER = 'gender'
    ADDRESS_1 = 'address_1'
    ADDRESS_2 = 'address_2'
    ADDRESS_3 = 'address_3'
    TOWN_CITY = 'town_city'
    COUNTY = 'county'
    COUNTRY = 'country'
    REGULAR_RESTAURANT = 'regular_restaurant'
