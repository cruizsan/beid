import json

import smartcard.System

from lib.beid import Beid

# informations only
result = Beid().read(smartcard.System.readers()[0], photo=False, informations=True, address=False)
print(json.dumps(result, indent=4))

"""
    "informations": {
        "nationality": "XXXXXXX",
        "card_number": "XXXXXXX",
        "suffix": "XXXXXXX",
        "birthdate": "22/XXXXXXX/1991",
        "first_name": "XXXXXXX",
        "national_number": "XXXXXXX",
        "start_date": "XXXXXXX",
        "end_date": "XXXXXXX",
        "sex": "XXXXXXX",
        "place_of_delivery": "XXXXXXX",
        "last_name": "XXXXXXX",
        "birthplace": "XXXXXXX"
    }
"""