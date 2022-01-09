#!/usr/bin/env python
# coding: utf-8
"""
    Simple script that listens for Hubitat data on the event websocket and then adds that data to an influxdb database.
    Note the env file should have "hubitat_ip", "influx_ip", "username", and "password".
"""
import json
from influxdb import InfluxDBClient
from time import time
import websocket
import logging
from logging.handlers import TimedRotatingFileHandler

def message_parser(message):
    """
    Exract info required for data insertion
    """
    logger.info(message)

    # Used to remap values if needed
    value_mapping = {
        "on": 1,
        "off": 0
    }

    measurement=message["name"]
    displayName=message["displayName"]
    value=message["value"]
    unit=message["unit"]
    did=message["deviceId"]
    timestamp=message["ts"]
    if value in value_mapping.keys():
        value = value_mapping[value]

    try:
        value=float(value)
    except ValueError as e:
        # YES I'm passing this - this is because the incoming value is actually a string, let it free
        pass

    if type(value) == str:
        line = f'{measurement},deviceId={did} value="{value}",unit="{unit}",displayName="{displayName}" {int(timestamp*1e9)}'
    else:
        line = f'{measurement},deviceId={did} value={value},unit="{unit}",displayName="{displayName}" {int(timestamp*1e9)}'
    return line

def insert_message(wsapp, message):
    """
    Write the message to the database after parsing
    """
    message = json.loads(message)
    message["ts"] = time()
    line = message_parser(message)
    client =InfluxDBClient(
        host=INFLUX_ADDR,
        port=8086,
        username=USER,
        password=PASS)

    client.write([line], {'db': 'hubitat'}, 204, 'line')
    client.close()

if __name__ == "__main__":

    env_file = '.env'
    with open(env_file) as f:
        env_data = json.load(f)
    HUB_ADDR = env_data["hubitat_ip"]
    INFLUX_ADDR = env_data["influx_ip"]
    USER = env_data["username"]
    PASS = env_data["password"]
    logpath = env_data["log_location"]

    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler(logpath,
                                       when="h",
                                       interval=1,
                                       backupCount=3)
    logger.addHandler(handler)

    logger.info("###### Starting Hubitat Logging #######")


    e_sock = f"ws://{HUB_ADDR}/eventsocket"

    wsapp = websocket.WebSocketApp(e_sock, on_message=insert_message)
    wsapp.run_forever()
