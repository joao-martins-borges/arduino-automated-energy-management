import time
import mysql.connector
import Comsuption
from Queues import solarStorage, eolicStorage, solarObject, eolicObject, requests, chargeTime, rules

dbhost = "localhost"
user = "python"
password = "python"
dbname = "dbsensores"


def runEnergyManagement():
    while True:
        try:

            time.sleep(0.5)
            solar = solarObject.storage
            eolic = eolicObject.storage
            solarValue = solarStorage.pop()
            solarStorage.clear()
            eolicValue = eolicStorage.pop()
            eolicStorage.clear()
            solarRule = int(rules['solar'])
            eolicRule = int(rules['eolic'])


            if int(solarValue) == 0:
                solarValue = "1"
            if int(eolicValue) == 0:
                eolicValue = "1"

            solarChargeTime = (100 - int(solar)) / (int(solarValue) * 0.1)
            eolicChargeTime = (100 - int(eolic)) / (int(eolicValue) * 0.1)

            dbconn = mysql.connector.connect(host=dbhost, user=user, password=password, database=dbname)
            c = dbconn.cursor()
            c.execute("CALL get_actuator_state('city_lights')")
            value = c.fetchone()
            while dbconn.next_result():
                print()

            if value[0] == 'on':
                lstate = True
            else:
                lstate = False

            c.execute("CALL get_actuator_state('watering')")
            value = c.fetchone()
            while dbconn.next_result():
                print()
            c.close()
            dbconn.close()

            if value[0] == 'on':
                wstate = True
            else:
                wstate = False

            consumeValue = Comsuption.getConsumption(lstate, wstate, chargeTime.consume)

            if chargeTime.passive:
                if eolicChargeTime <= solarChargeTime and eolic >= eolicRule and consumeValue <= eolic:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, True)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    if chargeTime.usage != "Eolic Energy":
                        chargeTime.setEnergy("Eolic Energy")
                        requests.insert(0,"eolic")
                elif eolicChargeTime >= solarChargeTime and solar >= solarRule and consumeValue <= solar:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, True)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)
                    if chargeTime.usage != "Solar Energy":
                        chargeTime.setEnergy("Solar Energy")
                        requests.insert(0, "solar")
                elif eolic >= eolicRule and solar <= solarRule and consumeValue <= eolic:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, True)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    if chargeTime.usage != "Eolic Energy":
                        chargeTime.setEnergy("Eolic Energy")
                        requests.insert(0,"eolic")
                elif solar >= solarRule and eolic <= eolicRule and consumeValue <= solar:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, True)
                    eolicObject.ConsumeEnergy(eolicValue,consumeValue, False)
                    if chargeTime.usage != "Solar Energy":
                        chargeTime.setEnergy("Solar Energy")
                        requests.insert(0, "solar")
                else:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    if chargeTime.usage != "Not Consuming":
                        chargeTime.setEnergy("Not Consuming")
                        requests.insert(0, "none")
            else:
                if eolic == 0 and solar != 0 and consumeValue <= solar:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, True)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)
                    requests.insert(0, "usersolar")
                elif solar == 0 and eolic != 0 and consumeValue <= eolic:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, True)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    requests.insert(0, "usereolic")
                elif (solar == 0 and eolic == 0) or (consumeValue >= solar and consumeValue >= eolic):
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    requests.insert(0, "usernone")
                elif chargeTime.usage == "Eolic Energy" and consumeValue <= eolic:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, True)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                elif chargeTime.usage == "Solar Energy" and consumeValue <= solar:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, True)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)
                else:
                    chargeTime.setChargeTime(solarChargeTime, eolicChargeTime)
                    solarObject.ConsumeEnergy(solarValue, consumeValue, False)
                    eolicObject.ConsumeEnergy(eolicValue, consumeValue, False)

        except:
            pass
