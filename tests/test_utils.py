import sys
sys.path.append("..")

from queue import Queue


class MockedConnectionManager:
    """
    A class that mocks the basics of the connection manager for
    testing from other functions/classes
    """
    def __init__(self):
        self.has_initialized = False
        self.msg_queue = Queue()
        self.sent: list[(str, int)] = []

    def initialize(self):
        self.has_initialized = True

    def send(self, to: str, clock: int):
        self.sent.append((to, clock))