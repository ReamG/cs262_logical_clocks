import sys
import consts
import pdb
from connection_manager import ConnectionManager
from utils import print_error

class Machine:
    """
    A machine that will be used in our scale model. It will
    be instantiated with a name, which must be in the mapping
    given in the constants file. It will participate in communication
    and clock events as described in the specification.
    """

    def __init__(self, name: str):
        """
        Simply loads the identity with the given name. Throws an
        error if the name is not valid.
        NOTE: Does not do any work to establish connections.
        """
        if name not in consts.IDENTITY_MAP:
            raise ValueError("Invalid machine name")
        self.identity = consts.IDENTITY_MAP[name]
        self.conman = ConnectionManager(self.identity)
    
    def start(self):
        """
        Starts the machine
        """
        self.conman.initialize()
    
    def kill(self):
        """
        Kills the machine
        """
        self.conman.kill()


def create_machine(name: str):
    """
    Creates and runs a machine with the given name
    """
    try:
        machine = Machine(name)
        machine.start()
        machine.kill()
    except Exception as e:
        print_error("Unknown error")
        print(e.args)
        exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_error("Usage: python3 machine.py <machine_name>")
        exit(1)
    create_machine(sys.argv[1])    
