import json

import smartcard.System

from lib.beid import Beid

# address only
result = Beid().read(smartcard.System.readers()[0], photo=False, informations=False, address=True)
print(json.dumps(result, indent=4))

"""
    "address": {
        "address": "XXXXXXX",
        "locality": "XXXXXXX",
        "postal_code": "XXXXXXX"
    }
"""