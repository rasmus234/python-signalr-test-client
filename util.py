from threading import Lock

from signalrcore.hub.base_hub_connection import BaseHubConnection


def on_result(message):
    print(message.result)


def send(connection: BaseHubConnection, method: str, args: []):
    result = connection.send(method, args, lambda m: on_result(m))
