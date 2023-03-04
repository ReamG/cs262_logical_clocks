import socket
import threading
import consts
import time
from pudb import forked
from typing import Mapping
from schema.identity import Identity
from threading import Thread
from utils import print_info, print_error

class ConnectionManager:
    """
    Handles the dirty work of opening sockets to the other machines.
    Abstracts to allow machines to operate at the level of sending
    messages based on machine name, ignoring underlying sockets.
    """

    def __init__(self, identity: Identity):
        self.identity = identity
        self.socket_map: Mapping[str, any] = {}
        self.alive = True
    
    def kill(self):
        """
        Kills the connection manager
        """
        self.alive = False
        for sock in self.socket_map.values():
            sock.shutdown(1)
            sock.close()
    
    def consume(self, conn, name):
        """
        Once a connection is established, open a thread that continuously
        listens for incoming messages
        conn: connection object
        name: name of the machine that connected
        """
        print(f"Listening for messages from {name} on {self.identity.name}...")
        try:
            conn.settimeout(1)
            while True:
                # Get the message
                msg = conn.recv(1024).decode()
                if msg and len(msg) > 0:
                    print_info(f"Received message from {name}: {msg}")
        except socket.timeout:
            if not self.alive:                
                conn.close()
                return
        except:
            conn.close()
    
    def handle_consumers(self):
        """
        Once connections are established, opens a new thread just
        to handle the consumption of messages
        """
        for (name, sock) in self.socket_map.items():
            consumer_thread = Thread(
                target=self.consume,
                args=(sock, name)
            )
            consumer_thread.start()
    
    def listen(self):
        """
        Listens for incoming connections
        """
        # Setup the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.identity.host_ip, self.identity.host_port))
        sock.listen()
        # Listen the specified number of times
        listens_completed = 0
        while listens_completed < self.identity.num_listens:
            # Accept the connection
            conn, addr = sock.accept()
            # Get the name of the machine that connected
            name = conn.recv(1024).decode()
            # Add the connection to the map
            self.socket_map[name] = conn
            listens_completed += 1
        try:
            sock.shutdown(1)
        except:
            pass
        sock.close()

    def connect(self, name: str):
        """
        Connects to the machine with the given name
        """
        # Get the identity of the machine to connect to
        identity = consts.IDENTITY_MAP[name]
        # Setup the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((identity.host_ip, identity.host_port))
        # Send the name of this machine
        sock.send(self.identity.name.encode())
        # Add the connection to the map
        self.socket_map[name] = sock
    
    def handle_connections(self):
        """
        Handles the connections to other machines
        """
        # Connect to the machines in the connection list
        for name in self.identity.connections:
            connected = False
            while not connected:
                try:
                    self.connect(name)
                    connected = True
                except:
                    print_error(f"Failed to connect to {name}, retrying in 1 second")
                    time.sleep(1)
    
    def initialize(self):
        """
        Does the work of initializing the connection manager
        """
        listen_thread = Thread(target=self.listen)
        connect_thread = Thread(target=self.handle_connections)

        listen_thread.start()
        connect_thread.start()

        listen_thread.join()
        connect_thread.join()

        self.handle_consumers()