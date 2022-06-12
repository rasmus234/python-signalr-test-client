import json
import logging
import random
import sys
import time

from signalrcore.messages.completion_message import CompletionMessage

import util

sys.path.append("./")
from signalrcore.hub_connection_builder import *


logger_id = "62a5e6512870a77e7aaf4ff0"
data = {
   "Logging":{
      "LoggerId":logger_id,
      "PairingId":"",
      "Active":True,
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
def calibrate(param):
    data["Soil"][param] = 1.2
    util.send(hub_connection,"SendConfig", [data])


def serialize(data):
    print(data)
    # print(json.dumps(data))

def start_listener():
    hub_connection.on("ReceiveMessage", print)
    argss = None
    # response = hub_connection.send("ConnectLogger", ["rasmus","id"], lambda args: print(args.result))

    util.send(hub_connection,"ConnectLogger", [logger_id])
    # util.send(hub_connection,"ConnectLogger", ["62a1ec85e74a66e76deaWRONMG"])
    hub_connection.on("GetConfig", lambda response: util.send(hub_connection,"SendConfig", [data]))
    hub_connection.on("SetConfig", serialize)
    hub_connection.on("Calibrate", lambda response: calibrate(response[0]))

    # response = hub_connection.send("ConnectLogger", ["TestId"])




server_url = "ws://localhost:5140/hubs/logger"
# server_url = "https://plant-control-backend.herokuapp.com/hubs/logger"
# server_url = "http://20.4.59.10:9093/hubs/logger"

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
