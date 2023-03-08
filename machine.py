import sys
import consts
import time
import random
import math
from connection_manager import ConnectionManager
from utils import print_error

class Machine:
    """
    A machine that will be used in our scale model. It will
    be instantiated with a name, which must be in the mapping
    given in the constants file. It will participate in communication
    and clock events as described in the specification.
    """

    def __init__(self, name: str, run: int, start_time: int):
        """
        Simply loads the identity with the given name. Throws an
        error if the name is not valid.
        NOTE: Does not do any work to establish connections.
        NOTE: Run is the run number, used to distinguish between
        different runs of the same machine (mostly for file naming purposes)
        """
        if name not in consts.IDENTITY_MAP:
            raise ValueError("Invalid machine name")
        self.identity = consts.IDENTITY_MAP[name]
        self.run = run
        self.start_time = start_time
        self.conman = ConnectionManager(self.identity)
        self.ticks_per_second = random.randint(1, 6)
        self.clock = 0
        # Helper variable to keep track of list of other machine names
        self.others = consts.get_other_machines(name)
    
    def get_system_time(self):
        """
        Helper function to return the system time in milliseconds
        """
        return consts.get_time() - self.start_time
    
    def start(self):
        """
        Starts the machine
        """
        self.conman.initialize()
        self.fout = open(f"output/{self.identity.name}{self.run}.out", "w")
        self.fout.write(f"INIT,{self.identity.name},{self.ticks_per_second}\n")
        self.loop()
    
    def receive_message(self):
        """
        Tries to receive a single message from the network queue. If the
        queue is empty, does nothing. Otherwise, it takes the message from
        the queue, updates the logical clock, and write to the output file.
        What does it write?
        RECEIVED, SENDER, MSG_Q_LENGTH, GLOBAL_TIME, LOGICAL_TIME
        NOTE: It's expected that this function is only called when the queue
        is non-empty. The check's here are just to cover bases/for safety.
        """
        if self.conman.msg_queue.empty():
            return False
        msg = self.conman.msg_queue.get()
        self.clock = max(self.clock, msg.time) + 1
        self.fout.write(f"RECEIVED,{msg.author},{self.conman.msg_queue.qsize()},{self.get_system_time()},{self.clock}\n")
        return True

    def single_send(self, to: str):
        """
        Sends a message to one peer
        What does it write?
        SINGLE_SEND, TO, SYSTEM_TIME, LOGICAL_TIME
        """
        if to not in self.others:
            raise ValueError("Invalid machine name")
        self.conman.send(to, self.clock)
        self.fout.write(f"SINGLE_SEND,{self.get_system_time()},{self.clock}\n")
    
    def multi_send(self):
        """
        Sends a message to two peers
        What does it write?
        MULTI_SEND, SYSTEM_TIME, LOGICAL_TIME
        """
        others = consts.get_other_machines(self.identity.name)
        for other in others:
            self.conman.send(other, self.clock)
        self.fout.write(f"MULTI_SEND,{self.get_system_time()},{self.clock}\n")
    
    def internal_event(self):
        """
        Performs an internal event
        What does it write?
        INTERNAL_EVENT, SYSTEM_TIME, LOGICAL_TIME
        """
        self.fout.write(f"INTERNAL_EVENT,{self.get_system_time()},{self.clock}\n")

    def frame(self):
        """
        A single step of the machine, seen abstractly as one unit of time in 
        the logical clock. 
        """
        if not self.conman.msg_queue.empty():
            self.receive_message()
            return
        # Msg queue empty, update the clock and take an action
        self.clock += 1
        action = random.randint(1, 10)
        if action == 1:
            self.single_send(self.others[0])
        elif action == 2:
            self.single_send(self.others[1])
        elif action == 3:
            self.multi_send()
        else:
            self.internal_event()

    def loop(self):
        """
        A function that regulates the speed of the machine and ensure's that
        only `ticks_per_second` ticks are executed per second.
        """
        milliseconds_per_tick = math.ceil(1000 / self.ticks_per_second)
        while consts.get_time() - self.start_time < consts.EXPERIMENT_DURATION:
            frame_start = consts.get_time()
            self.frame()
            sleep_amt = milliseconds_per_tick - (consts.get_time() - frame_start)
            if sleep_amt > 0:
                time.sleep(sleep_amt / 1000)
    
    def kill(self):
        """
        Kills the machine
        """
        self.conman.kill()
        self.fout.close()


def create_machine(name: str, run: int, start_time: int):
    """
    Creates and runs a machine with the given name
    NOTE: start_time is milliseconds since epoch from
    the `runner.py` script to coordinate system time across processes
    """
    try:
        machine = Machine(name, run, start_time)
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
