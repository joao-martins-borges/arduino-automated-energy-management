from time import sleep

from Queues import requests


def runRequests(s):
    while True:
        if len(requests) > 0:
            pedido = requests.pop()
            s.send(pedido.encode())
            print("ENVIEI PEDIDO: " + pedido)
            sleep(0.1)
        else:
            sleep(1)
