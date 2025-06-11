#!/usr/bin/env python
import random

from Queues import requests, responses
import serial
import time
import sys

#Important variables
usbport = 'COM3'
hostname = 'localhost'

#Important connections
ser = serial.Serial(usbport, 9600, timeout=1)

aux = 1

def listenArduino():
    #CODIGO PARA ARDUINO
    while True:
        ser.flushInput
        if len(requests)>0:
            #Check for new requests
            request = requests.pop()
            ser.write(request.encode())
            if request=="watering" or request=="userwatering":
                time.sleep(0.4)
        else:
            #Send request to Arduino
            ser.write("read".encode())

        #Wait for response
        
        time.sleep(0.1)
        line = ser.readline().decode('ascii')
        ser.flushOutput
        print("Arduino response -> "+line)
        if line != "":
            if line == "City lights on":
                responses.insert(0,"clon")
            elif line == "City lights off":
                responses.insert(0,"cloff")
            elif line == "solar":
                responses.insert(0,"solar")
            elif line == "eolic":
                responses.insert(0,"eolic")
            elif line == "none":
                responses.insert(0,"none")
            elif line == "watering":
                responses.insert(0,"watering")
            elif line == "passiveOn":
                responses.insert(0,"passiveOn")
            elif line == "passiveOff":
                responses.insert(0,"passiveOff")
            elif line.split("-")[0] == "r":
                response = line  
                responses.insert(0,response)


