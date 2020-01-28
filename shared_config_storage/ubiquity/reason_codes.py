from enum import Enum
from typing import Tuple

REASON_CODES = (
    ('X000', 'New data submitted/modified'),
    ('X100', 'Add fields being validated'),
    ('X101', 'Account does not exist'),
    ('X102', 'Add data rejected by merchant'),
    ('X103', 'No authorisation provided'),
    ('X104', 'Update failed. Delete and re-add card.'),
    ('X105', 'Account not registered'),
    ('X200', 'Enrolment in progress'),
    ('X201', 'Enrolment data rejected by merchant'),
    ('X202', 'Account already exists'),
    ('X203', 'Enrolment complete'),
    ('X300', 'Authorisation correct'),
    ('X301', 'Authorisation in progress'),
    ('X302', 'No authorisation required'),
    ('X303', 'Authorisation data rejected by merchant'),
    ('X304', 'Authorisation expired')
)

CURRENT_STATUS_CODES = (
    (0, 'Pending'),
    (1, 'Active'),
    (5, 'Please check your scheme account login details.'),
    (9, 'Midas unavailable'),
    (10, 'Wallet only card'),
    (204, 'Pending manual check'),
    (401, 'Failed validation'),
    (403, 'Invalid credentials'),
    (404, 'Agent does not exist on midas'),
    (406, 'Pre-registered card'),
    (429, 'Cannot connect, too many retries'),
    (432, 'Invalid mfa'),
    (434, 'Account locked on end site'),
    (436, 'Invalid card_number'),
    (437, 'You can only Link one card per day.'),
    (438, 'Unknown Card number'),
    (439, 'General Error such as incorrect user details'),
    (441, 'Join in progress'),  # Error raised by Iceland when attempting second join during a join in progress
    (442, 'Asynchronous join in progress'),
    (444, 'No user currently found'),
    (445, 'Account already exists'),
    (446, 'Update failed. Delete and re-add card.'),
    (447, 'Scheme requested account deletion'),
    (503, 'Too many balance requests running'),
    (520, 'An unknown error has occurred'),
    (530, 'End site down'),
    (531, 'IP blocked'),
    (532, 'Tripped captcha'),
    (533, 'Password expired'),
    (535, 'Request was not sent'),
    (536, 'Error with the configuration or it was not possible to retrieve'),
    (537, 'Service connection error'),
    (538, 'A system error occurred during join'),
    (900, 'Join'),
    (901, 'Join Failed')
)

reason_code_translation = {
    0: 'X100',
    1: 'X300',
    5: 'X303',
    9: None,
    10: 'X103',
    204: 'X100',
    401: None,
    403: 'X303',
    404: 'X101',
    406: 'X105',
    429: None,
    432: 'X303',
    434: 'X304',
    436: 'X102',
    437: None,
    438: 'X105',
    439: None,
    441: 'X201',
    442: 'X100',
    444: 'X101',
    445: 'X202',
    446: 'X104',
    447: 'X304',
    503: None,
    520: None,
    530: None,
    531: None,
    532: None,
    533: 'X304',
    535: None,
    536: None,
    537: None,
    538: None,
    900: 'X201',
    901: 'X201'
}

ubiquity_status_translation = {
    0: 'pending',
    1: 'authorised',
    5: 'unauthorised',
    9: 'failed',
    10: 'pending',
    204: 'pending',
    401: 'failed',
    403: 'failed',
    404: 'unauthorised',
    406: 'failed',
    429: 'failed',
    432: 'unauthorised',
    434: 'failed',
    436: 'failed',
    437: 'failed',
    438: 'failed',
    439: 'failed',
    441: 'failed',
    442: 'pending',
    444: 'failed',
    445: 'failed',
    446: 'failed',
    447: 'failed',
    503: 'failed',
    520: 'failed',
    530: 'failed',
    531: 'failed',
    532: 'failed',
    533: 'unauthorised',
    535: 'failed',
    536: 'failed',
    537: 'failed',
    538: 'failed',
    900: 'failed',
    901: 'failed'
}


def get_state_and_reason_code(status_code: int) -> Tuple[str, str]:
    state = ubiquity_status_translation[status_code]
    reason_code = reason_code_translation[status_code]
    return state, reason_code


class StatusCodes(Enum):
    PENDING = 0
    # todo add statuses as needed
