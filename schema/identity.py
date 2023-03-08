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
        # The name of the machine (in our experiments "A" | "B" | "C")
        self.name = name
        # The ip address the machine should listen on for new connections
        self.host_ip = host_ip
        # The port the machine should listen on for new connections
        self.host_port = host_port
        # The number of connections the machine should listen for
        self.num_listens = num_listens
        # The names of the machines that this machine should connect to
        self.connections = connections
