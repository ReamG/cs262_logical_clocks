import asyncio
import time
import numpy as np
import grpc
import consts
from parent_wire import schema_pb2 as schema, schema_pb2_grpc as services, 
from communication import PeerConnection
from typing import Optional

class Machine():
    """
    A class to simulate a single machine object in our scale model
    """

    def __init__(self, rate):
        self.log = []
        self.rate: int = rate
        self.peer_connections: list[PeerConnection] = []
        self.identity: Optional[schema.Identity] = None

    def identify(self):
        """
        Establishes a stub with the parent process to get an identity,
        peers, and a stub to communicate with the parent
        returns: (identity, peers, stub)
        """
        with grpc.insecure_channel(consts.PARENT_IP + f":{consts.PARENT_PORT}") as channel:
            stub = services.ParentStub(channel=channel)
            response = stub.ImAlive(schema.ImAliveRequest())
            return (response.identity, response.peers)
    
    async def establish_connections(self):
        """
        This function handles the logic of connecting to our peers.
        It will first try to connect to all peers that already exist,
        then will start listening until we have reached the maximum
        """
        # First introduce ourselves to peers that already exist
        for peer in self.peers:
            connection = PeerConnection(peer)
            await connection.try_establish()
            self.peer_connections.append(connection)
        # Then listen for new peers
        while len(self.peer_connections) < consts.MAX_CLIENTS:
            def on_connect(reader, writer):
                self.peer_connections.append(PeerConnection(peer, reader, writer))
            await PeerConnection.listen(50052, on_connect)

    def start(self):

        (self.identity, self.peers) = self.identify()

        with grpc.insecure_channel(consts.PARENT_IP + f":{consts.PARENT_PORT}") as channel:
            self.stub = services.ParentStub(channel=channel)
            self.stub.ImDying(self.identity)

if __name__ == "__main__":
    machine = Machine(1)
    machine.start()