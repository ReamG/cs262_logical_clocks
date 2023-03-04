import asyncio
from asyncio.streams import _ClientConnectedCallback
import consts
from typing import Optional, Mapping
from parent_wire import schema_pb2 as schema, schema_pb2_grpc as services
from time import sleep
    
class PeerConnection:
    """
    A class to handle the connection to a peer
    """

    def __init__(
            self, 
            identity: schema.Identity, 
            reader: Optional[asyncio.StreamReader] = None, 
            writer: Optional[asyncio.StreamWriter] = None
        ):
        self.identity: schema.Identity = identity
        self.reader = reader
        self.writer = writer

    @staticmethod
    async def try_establish(identity: schema.Identity):
        """
        Makes a single attempt to establish a connection to the peer
        NOTE: Can throw an error, this must be called by a try/except block
        """
        (reader, writer) = await asyncio.open_connection(consts.MACHINE_IP, identity.port)
        writer.write("test")
        await writer.drain()
        return (reader, writer)

    @staticmethod
    async def listen(port, callback):
        """
        A method called that will listen for a sigle connection
        """
        # Intercepts the callback to 
        async def intercept_callback(reader, writer):
            str = await reader.read()
            print("got " + str)
            callback(reader, writer, str)
        await asyncio.start_server(callback, consts.MACHINE_IP, port)

class ConnectionManager:
    """
    A class to manage a set of connections to peers
    """
    
    def __init__(self, identity: schema.Identity, peers: list[schema.Identity]):
        self.identity: schema.Identity = identity
        self.peers: list[schema.Identity] = peers
        self.connections: Mapping[str, PeerConnection] = {}
    
    async def connect_to_peer(self, peer):
        """
        Connects to a peer
        """
        while not peer.name in self.connections[peer.name] and max:
            try:
                reader, writer = await PeerConnection.try_establish(peer)
                self.connections[peer.name] = PeerConnection(peer, reader, writer)
            except:
                sleep(1)

    await def establish_connections(self):


async def test():
    identity1 = schema.Identity(name="test1", port=50052)
    identity2 = schema.Identity(name="test2", port=50053)
    connection1 = PeerConnection(identity1)
    connection2 = PeerConnection(identity1)
    await connection1.try_host()
    await connection2.try_establish()
    
asyncio.run(test())
