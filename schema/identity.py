from __future__ import annotations

class Identity:
    """
    A class that represents the identity of a machine. Most crucially
    this stores information about which ip/port the machine is listening
    on, as well as which other machines it is responsible for connecting
    to.
    """
    def __init__(
            self,
            name: str,
            host_ip: str,
            host_port: str,
            num_listens: int,
            connections: list[str]
        ):
        self.name = name
        self.host_ip = host_ip
        self.host_port = host_port
        self.num_listens = num_listens
        self.connections = connections
