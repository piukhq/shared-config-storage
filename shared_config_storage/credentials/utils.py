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


class CredentialType(str, Enum):
    USER_NAME = 'username'
    CARD_NUMBER = 'card_number'
    BARCODE = 'barcode'
    PASSWORD = 'password'
    PLACE_OF_BIRTH = 'place_of_birth'
    EMAIL = 'email'
    POSTCODE = 'postcode'
    MEMORABLE_DATE = 'memorable_date'
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
    MERCHANT_IDENTIFIER = 'merchant_identifier'
    PAYMENT_CARD_ID = 'payment_card_id'


class EncryptedCredentials(Enum):
    PASSWORD = CredentialType.PASSWORD.value
    POSTCODE = CredentialType.POSTCODE.value
    MEMORABLE_DATE = CredentialType.MEMORABLE_DATE.value
    PLACE_OF_BIRTH = CredentialType.PLACE_OF_BIRTH.value
    PIN = CredentialType.PIN.value
    TITLE = CredentialType.TITLE.value
    FIRST_NAME = CredentialType.FIRST_NAME.value
    LAST_NAME = CredentialType.LAST_NAME.value
    FAVOURITE_PLACE = CredentialType.FAVOURITE_PLACE.value
    DATE_OF_BIRTH = CredentialType.DATE_OF_BIRTH.value
    PHONE = CredentialType.PHONE.value
    PHONE_2 = CredentialType.PHONE_2
    GENDER = CredentialType.GENDER.value
    ADDRESS_1 = CredentialType.ADDRESS_1.value
    ADDRESS_2 = CredentialType.ADDRESS_2.value
    ADDRESS_3 = CredentialType.ADDRESS_3.value
    TOWN_CITY = CredentialType.TOWN_CITY.value
    COUNTY = CredentialType.COUNTY.value
    COUNTRY = CredentialType.COUNTRY.value
    REGULAR_RESTAURANT = CredentialType.REGULAR_RESTAURANT.value
