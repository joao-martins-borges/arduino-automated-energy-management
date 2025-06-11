import socket
from ClientRequests import createClient
from ArduinoResponse import arduinoConnect
from threading import Thread
from ArduinoHandler import listenArduino

hostname = '0.0.0.0'
port = 8000

def clientConnection(c):
    createClient(c)

def arduinoConnection(c):
    arduinoConnect(c)

if __name__ == '__main__':
    try:
        listen_arduino = Thread(target=listenArduino)
        listen_arduino.start()
        
        s = socket.socket()
        s.bind((hostname, port))
        s.listen()

        while True:
            c, addr = s.accept()
            print('Got connection from', addr)

            #Create and Run threads for client and arduino server connections
            th = Thread(target=clientConnection, args=(c,))
            ar = Thread(target=arduinoConnection, args=(c,))
            th.start()
            ar.start()
    except KeyboardInterrupt:
        print("Error")
