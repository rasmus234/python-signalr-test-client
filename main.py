import logging
import sys
import time

from signalrcore.messages.completion_message import CompletionMessage

sys.path.append("./")
from signalrcore.hub_connection_builder import *


def start_listener():
    hub_connection.on("ReceiveMessage", print)
    argss = None
    response = hub_connection.send("ConnectLogger", ["rasmus","id"], lambda args: print(args.result))
    print(response)



server_url = "ws://localhost:5140/hubs/logger"

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
hub_connection: BaseHubConnection = HubConnectionBuilder() \
    .with_url(server_url, options={"verify_ssl": False}) \
    .configure_logging(logging.ERROR, socket_trace=True, handler=handler) \
    .with_automatic_reconnect({
    "type": "interval",
    "keep_alive_interval": 10,
    "intervals": [1, 3, 5, 6, 7, 87, 3]
}).build()

hub_connection.start()
hub_connection.on_open(start_listener)
hub_connection.on_close(lambda: print("connection closed"))

while True:
    continue

sys.exit(0)
