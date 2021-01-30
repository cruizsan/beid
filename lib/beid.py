import json


class Beid:
    _id = [0x3F, 0x00, 0xDF, 0x01, 0x40, 0x31]
    _address = [0x3F, 0x00, 0xDF, 0x01, 0x40, 0x33]
    _photo = [0x3F, 0x00, 0xDF, 0x01, 0x40, 0x35]
    _mois = {
        "JANV": "01",
        "JAN": "01",
        "FEVR": "02",
        "FEV": "02",
        "MARS": "03",
        "MAR": "03",
        "AVRI": "04",
        "AVR": "04",
        "MAI": "05",
        "JUIN": "06",
        "JUIL": "07",
        "AOUT": "08",
        "AOU": "08",
        "SEPT": "09",
        "SEP": "09",
        "OCTO": "10",
        "OCT": "10",
        "NOVE": "11",
        "NOV": "11",
        "DECE": "12",
        "DEC": "12"
    }

    def read(self, device, informations=True, address=True, photo=True):
        try:
            cnx = device.createConnection()
            cnx.connect()
            users_informations = {}
            if informations:
                users_informations['informations'] = self._read_informations(cnx)
            if address:
                users_informations['address'] = self._read_address(cnx)
            if photo:
                users_informations['photo'] = self._read_photos(cnx)
            return users_informations
        except Exception as e:
            print(json.dumps({"error": e}), flush=True)

    def _read_informations(self, cnx):
        cmd = [0x00, 0xA4, 0x08, 0x0C, len(self._id)] + self._id
        # select file : informations
        data, sw1, sw2 = cnx.transmit(cmd)

        # read file
        cmd = [0x00, 0xB0, 0x00, 0x00, 256]
        data, sw1, sw2 = cnx.transmit(cmd)
        if "%x" % sw1 == "6c":
            cmd = [0x00, 0xB0, 0x00, 0x00, sw2]
            data, sw1, sw2 = cnx.transmit(cmd)
            idx = 0
            num_info = 0
            infos = []
            while num_info <= 12:
                num_info = data[idx]
                idx += 1
                len_info = data[idx]
                idx += 1
                chaine_bytes = []
                for x in range(len_info):
                    chaine_bytes.append(data[idx])
                    idx += 1
                try:
                    infos.append(bytes(chaine_bytes).decode("utf-8"))
                except UnicodeDecodeError:
                    infos.append(u"")
            return {
                "card_number": infos[0],
                "start_date": infos[2].replace(".", "/"),
                "end_date": infos[3].replace(".", "/"),
                "place_of_delivery": infos[4],
                "national_number": infos[5],
                "last_name": infos[6],
                "first_name": infos[7],
                "suffix": infos[8],
                "nationality": infos[9],
                "birthplace": infos[10],
                "birthdate": infos[11].split()[0] + "/" + self._mois[infos[11].split()[1]] + "/" +
                             infos[11].split()[2],
                "sex": infos[12],
            }
        return {}

    def _read_address(self, cnx):
        # select file : address
        cmd = [0x00, 0xA4, 0x08, 0x0C, len(self._address)] + self._address
        data, sw1, sw2 = cnx.transmit(cmd)

        # read file
        cmd = [0x00, 0xB0, 0x00, 0x00, 256]
        data, sw1, sw2 = cnx.transmit(cmd)
        if "%x" % sw1 == "6c":
            cmd = [0x00, 0xB0, 0x00, 0x00, sw2]
            data, sw1, sw2 = cnx.transmit(cmd)
            idx = 0
            num_info = 0
            infos = []
            while num_info <= 2:
                num_info = data[idx]
                idx += 1
                len_info = data[idx]
                idx += 1
                chaine_bytes = []
                for x in range(len_info):
                    chaine_bytes.append(data[idx])
                    idx += 1
                try:
                    infos.append(bytes(chaine_bytes).decode("utf-8"))
                except UnicodeDecodeError:
                    infos.append(u"")
            return {
                "address": infos[0],
                "postal_code": infos[1],
                "locality": infos[2]
            }
        return {}

    def _read_photos(self, cnx):
        # select file : photo
        cmd = [0x00, 0xA4, 0x08, 0x0C, len(self._photo)] + self._photo
        data, sw1, sw2 = cnx.transmit(cmd)

        photo_bytes = []

        offset = 0
        while "%x" % sw1 == "90":
            cmd = [0x00, 0xB0, offset, 0x00, 256]
            data, sw1, sw2 = cnx.transmit(cmd)
            photo_bytes += data
            offset += 1
        if "%x" % sw1 == "6c":
            offset -= 1
            cmd = [0x00, 0xB0, offset, 0x00, sw2]
            data, sw1, sw2 = cnx.transmit(cmd)
            photo_bytes += data

        photo = bytearray(photo_bytes)
        return photo