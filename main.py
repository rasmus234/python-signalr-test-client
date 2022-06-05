import logging
import sys
import time

sys.path.append("./")
from signalrcore.hub_connection_builder import *


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


server_url = "ws://localhost:5140/hubs/unregisteredLogger"

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
hub_connection:BaseHubConnection = HubConnectionBuilder()\
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
    .with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        }).build()

hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
hub_connection.on_close(lambda: print("connection closed"))

hub_connection.on("ReceiveMessage", print)
hub_connection.start()
hub_connection.on_open(lambda: hub_connection.send("ConnectUnregisteredLogger", []))

# Do login
while True:
    continue

sys.exit(0)