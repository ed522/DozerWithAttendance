import logging
import json
import socket
import socketserver
import threading
from operator import truediv

from dotenv import load_dotenv

load_dotenv()

def run():
    # Specs:
    #
    # A screen sends out a 255.255.255.255 broadcast app: attendance, type: discovery, version: 1 (as of now), host matching local IP
    # Server connects to host given in the parameter
    #
    # On connect, screen sends JSON object with type = "connect"
    # Server sends type = "acknowledge", targeting = "connect"
    # On every code generation event (screen): type = "code", code = <generated code>, generation_time = <generation Unix timestamp>
    # Server acknowledges with type = "acknowledge", targeting = "code", code = <same>, valid_to = <expiry time>
    # Every 10s, screen sends type = "heartbeat", counter = <counter that increments each heartbeat>
    # Server sends type = "acknowledge", targeting = "heartbeat", counter = <counter>
    #
    # Errors:
    # If the heartbeat counters do not match, server sends type = "heartbeat_error", counter = <corrected value>
    # If connection fails, disconnect and try again after 10s
    #
    # Note that the "server" here is the discord bot, but the server is technically the tablet
    def _communicate():
        broadcast_in_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        broadcast_in_sock.connect(('0.0.0.0', 5789))

    thread = threading.Thread(target=_communicate, daemon=True)
    thread.start()

def _discover(sock: socket.socket):

    const_version = 1

    while True:
        message = json.loads(sock.recv) #something? TODO FIX
        if message['app'] == 'attendance' and message['type'] == 'discovery' and message['version'] == const_version:
            return message['host']

def _communicate_after_handshake(request):

    const_code_valid_duration = 30 # seconds

    counter = 0

    connect_message = json.loads(request.recv(256))
    if connect_message['type'] != 'connect':
        logging.log(logging.ERROR, f"Failed to connect with client, wrong type {connect_message['type']}")
        return  # let client try again after 10s

    response = {
        'type': 'acknowledge',
        'targeting': connect_message['type']
    }
    request.sendall(json.dumps(response))

    while True:
        message = json.loads(request.recv(256))

        if message['type'] == 'heartbeat':
            counter += 1
            if counter != message['counter']:
                response = {
                    'type': 'heartbeat_error',
                    'counter': counter
                }
                request.sendall(json.dumps(response))

                logging.log(logging.WARN,
                            f"Connection error with attendance code client: got counter {message['counter']}, expected {counter}")

            else:
                response = {
                    'type': 'acknowledge',
                    'targeting': message['type'],
                    'counter': counter
                }
                request.sendall(json.dumps(response))

        elif message['type'] == 'code':
            code = int(message['code'])
            generation_time = int(message['generation_time'])
            response = {
                'type': 'acknowledge',
                'targeting': message['type'],
                'code': code,
                'valid_to': generation_time + const_code_valid_duration
            }
            request.sendall(json.dumps(response))
            # TODO commit to a db somewhere

        else:
            logging.log(logging.WARN, f"Unknown message {message['type']}, ignoring")