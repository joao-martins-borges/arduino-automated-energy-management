from Queues import responses
import time


def arduinoConnect(conn):
    while True:
        if len(responses) > 0:
            response = responses.pop()
            time.sleep(0.1)
            conn.send(response.encode())
