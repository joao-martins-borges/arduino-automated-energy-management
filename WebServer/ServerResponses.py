import time
from threading import Thread

from Queues import mlights, rules, requests, solarStorage, eolicStorage, chargeTime
import mysql.connector

dbhost = "localhost"
user = "python"
password = "python"
dbname = "dbsensores"


def runResponses(s):
    db = mysql.connector.connect(
        host=dbhost,
        user=user,
        password=password,
        database=dbname
    )

    cursor = db.cursor()
    while True:
        try:
            resposta = s.recv(1024).decode()
            print("RESPOSTA: " + resposta)
            message = resposta.split('-')
            if message[0] == "r":
                mlights.insert(0,message[1])
                solarStorage.insert(0,message[1])
                cursor.execute("CALL insert_light_value('" + message[1] + "')")
                eolicStorage.insert(0, message[2])
                cursor.execute("CALL insert_wind_value('" + message[2] + "')")
                db.commit()
                chargeTime.setConsume(int(message[3]))
                if len(mlights) >= 2:
                    old = mlights.pop()
                    clights_trigger = rules['city_lights']
                    watering_trigger = rules['watering']
                    try:
                        if(int(old) >= int(clights_trigger) and int(clights_trigger) >= int(message[1])):
                            requests.insert(0,"clon")
                        elif(int(old) <= int(clights_trigger) and int(clights_trigger) <= int(message[1])):
                            requests.insert(0,"cloff")

                        if (int(old) >= int(watering_trigger) and int(watering_trigger) >= int(message[1])):
                            requests.insert(0, "watering")

                    except:
                        pass
            elif message[0] == "clon":
                cursor.execute("CALL actuator_on('city_lights')")
                db.commit()
            elif message[0] == "cloff":
                cursor.execute("CALL actuator_off('city_lights')")
                db.commit()
            elif message[0] == "watering":
                cursor.execute("CALL actuator_on('watering')")
                db.commit()
                t1 = Thread(target=watering_off)
                t1.start()
            elif message[0] == "solar":
                chargeTime.setEnergy("Solar Energy")
                cursor.execute("CALL actuator_on('solar')")
                cursor.execute("CALL actuator_off('eolic')")
                db.commit()
            elif message[0] == "eolic":
                chargeTime.setEnergy("Eolic Energy")
                cursor.execute("CALL actuator_on('eolic')")
                cursor.execute("CALL actuator_off('solar')")
                db.commit()
            elif message[0] == "none":
                chargeTime.setEnergy("Not Cosuming")
                cursor.execute("CALL actuator_off('eolic')")
                cursor.execute("CALL actuator_off('solar')")
                cursor.execute("CALL actuator_off('city_lights')")
                db.commit()
            elif message[0] == "passiveOn":
                cursor.execute("CALL actuator_on('passive')")
                chargeTime.passive = True
                db.commit()
            elif message[0] == "passiveOff":
                cursor.execute("CALL actuator_off('passive')")
                chargeTime.passive = False
                db.commit()
        except:
            pass

def watering_off():
    time.sleep(10)
    dbconn = mysql.connector.connect(host=dbhost,user=user,password=password,database=dbname)
    c = dbconn.cursor()
    c.execute("CALL actuator_off('watering')")
    dbconn.commit()
    c.close()
    dbconn.close()
