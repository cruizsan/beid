# /usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.beid import Beid
import json
import base64
import time
from smartcard.CardMonitoring import CardMonitor, CardObserver

class PrintObserver(CardObserver):
    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        try:
            if len(addedcards) >= 1:
                print(json.dumps({"action": "inserted"}), flush=True)
                datas = Beid().read(addedcards[0])
                datas['photo'] = base64.b64encode(datas['photo']).decode()
                print(json.dumps(datas), flush=True)

            elif len(removedcards) >= 1:
                print(json.dumps({"action": "removed"}), flush=True)
        except Exception as e:
            print(json.dumps({"action": "error"}), flush=True)

cardmonitor = CardMonitor()
cardobserver = PrintObserver()
cardmonitor.addObserver(cardobserver)

while True:
    time.sleep(1)
