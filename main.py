import logging
import sys
import time

from signalrcore.messages.completion_message import CompletionMessage

import util

sys.path.append("./")
from signalrcore.hub_connection_builder import *



data = {
   "Logging":{
      "LoggerId":"62a1ec85e74a66e76deaab34",
      "PairingId":"",
      "Active":False,
      "SocketUrl":"40.87.132.220:9093",
      "RestUrl":"40.87.132.220:9092"
   },
   "Air":{
      "MinHumid":1,
      "MaxHumid":1,
      "MinTemp":1,
      "MaxTemp":11
   },
   "Soil":{
      "Moist":1.2,
      "Dry":3.3
   }
}


def start_listener():
    hub_connection.on("ReceiveMessage", print)
    argss = None
    # response = hub_connection.send("ConnectLogger", ["rasmus","id"], lambda args: print(args.result))

    util.send(hub_connection,"ConnectLogger", ["62a1ec85e74a66e76deaab34"])
    # util.send(hub_connection,"ConnectLogger", ["62a1ec85e74a66e76deaWRONMG"])
    hub_connection.on("GetConfig", lambda m: util.send(hub_connection,"SendConfig", [data]))
    # response = hub_connection.send("ConnectLogger", ["TestId"])




# server_url = "ws://localhost:5140/hubs/logger"
server_url = "https://plant-control-backend.herokuapp.com/hubs/logger"

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
