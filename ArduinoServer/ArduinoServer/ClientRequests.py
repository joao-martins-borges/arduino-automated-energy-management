from Queues import requests


def createClient(conn):
    while True:
        pedido = conn.recv(1024).decode()
        requests.insert(0,pedido)
        print("Client request   -> " + pedido)
