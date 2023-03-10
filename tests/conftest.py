# A file to setup mocks to other modules to help with testing
from queue import Queue
import sys
sys.path.append("..")
from schema.identity import Identity
from schema.message import Message
from typing import Union

# References to the mocked module s
sock_module = type(sys)("socket")
rand_module = type(sys)("random")

# Dummy constants
class timeout(Exception):
    pass
sock_module.timeout = timeout

SOL_SOCKET = 0
SO_REUSEADDR = 0
AF_INET = 0
SOCK_STREAM = 0
sock_module.SOL_SOCKET = SOL_SOCKET
sock_module.SO_REUSEADDR = SO_REUSEADDR
sock_module.AF_INET = AF_INET
sock_module.SOCK_STREAM = SOCK_STREAM

class socket:
    """
    A class that simulates all the important aspects of a socket
    for testing purposes
    """

    def __init__(self, _, __):
        self.has_closed = False
        self.fake_sends = Queue()
        self.binded_to = None
        self.connected_to = None
        self.has_listened = False
        self.fake_connect_names = []
        self.sent: list[bytes] = []
    
    # HELPER FUNCTIONS

    def add_fake_send(self, msg: Union[Message,str]):
        """
        Makes it so the next call to recv will return the given message
        encoded as a bytestring
        """
        self.fake_sends.put(msg)
    
    def set_fake_accept_names(self, names: list[str]):
        """
        Makes it so the next call to accept will return a socket that
        will return the given name when recv is called
        """
        self.next_fake_connect_names = names

    # MOCKED FUNCTIONS
    
    def close(self):
        self.has_closed = True
    
    def recv(self, _):
        if self.has_closed:
            raise Exception("Socket has been closed")
        if self.fake_sends.empty():
            raise Exception("No more messages to send")
        msg = self.fake_sends.get()
        return str(msg).encode()

    def settimeout(self, _):
        pass

    def setsockopt(self, _, __, ___):
        pass
    
    def bind(self, tup):
        self.binded_to = tup
    
    def listen(self):
        self.has_listened = True
    
    def accept(self):
        new_sock = socket(0, 0)
        if len(self.next_fake_connect_names) <= 0:
            raise Exception("No more names to accept")
        new_sock.add_fake_send(self.next_fake_connect_names[0])
        self.next_fake_connect_names = self.next_fake_connect_names[1:]
        return new_sock, ""
    
    def connect(self, tup):
        self.connected_to = tup
    
    def send(self, bs: bytes):
        self.sent.append(bs)


next_rand_int = 2

def prime_randint(next_num):
    global next_rand_int
    next_rand_int = next_num

def randint(_, __):
    global next_rand_int
    return next_rand_int

sock_module.socket = socket
rand_module.randint = randint

sys.modules["socket"] = sock_module
sys.modules["random"] = rand_module