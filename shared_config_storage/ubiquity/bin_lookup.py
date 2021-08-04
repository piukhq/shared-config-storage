from collections import namedtuple

BinMatch = namedtuple("BinMatch", "type len value")

BIN_TO_PROVIDER = {
    "visa": [
        BinMatch(type="equal", len=1, value="4"),
    ],
    "amex": [BinMatch(type="equal", len=2, value="34"), BinMatch(type="equal", len=2, value="37")],
    "mastercard": [BinMatch(type="range", len=2, value=(51, 55)), BinMatch(type="range", len=4, value=(2221, 2720))],
}


def bin_to_provider(bin_first_six: str) -> str:
    match_to_first_6 = {
        "range": lambda match: match.value[0] <= int(bin_first_six[: match.len]) <= match.value[1],
        "equal": lambda match: bin_first_six[: match.len] == match.value,
    }

    for provider, values in BIN_TO_PROVIDER.items():
        for bin_match in values:
            if match_to_first_6[bin_match.type](bin_match):
                return provider

    return "other"
