import smartcard.System

from lib.beid import Beid

# photo only
result = Beid().read(smartcard.System.readers()[0], informations=False, address=False, photo=True)
print(result)
f = open('result.jpg', 'wb')
f.write(result['photo'])
print("file generated")

"""
    {
        'photo': bytearray(b'XXXXXXXXXXXXXXXX')
    }
"""