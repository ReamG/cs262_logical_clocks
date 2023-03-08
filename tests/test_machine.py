import sys
sys.path.append("..")
from schema.identity import Identity
from schema.message import Message
from connection_manager import ConnectionManager
from machine import Machine
import consts
from threading import Thread
from test_utils import MockedConnectionManager
from queue import Queue
from conftest import prime_randint

BLANK_IDENTITY = Identity(
    name="T",
    host_ip="localhost",
    host_port=50052,
    num_listens=0,
    connections=[]
)

def test_init():
    """
    Tests that initialization works
    """

    # Test that you can only initialize with a valid identity
    errored = False
    try:
        Machine("not real", 1, 0)
    except:
        errored = True
    assert errored == True

    errored = False
    try:
        machA = Machine("A", 1, 0)
        Machine("B", 1, 0)
        Machine("C", 1, 0)
    except:
        errored = True
    assert errored == False

    # Test that all class values are properly set in init
    assert machA.identity == consts.IDENTITY_A
    assert machA.run == 1
    assert machA.start_time == 0
    assert type(machA.ticks_per_second) == int
    assert 1 <= machA.ticks_per_second <= 6
    assert machA.clock == 0
    assert machA.others == ["B", "C"]

    # Test that you can hardcode the ticks per second
    machB = Machine("B", 1, 0, 3)
    assert machB.ticks_per_second == 3

    # Test that if you don't hardcode the ticks per second, it's random
    prime_randint(1)
    machC = Machine("C", 1, 0)
    assert machC.ticks_per_second == 1

def test_get_system_time():
    """
    Tests that the get_system_time function works
    """
    machA = Machine("A", 1, 0)
    assert machA.get_system_time() == consts.get_time()

def test_start():
    """
    Tests that the start function works
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()

    # Make sure log file is not opened until start
    has_errored = False
    try:
        machA.fout.write("test")
    except:
        has_errored = True
    assert has_errored == True

    # To keep track of whether the loop function has been called
    has_called_loop = False
    def dummy_loop():
        nonlocal has_called_loop
        has_called_loop = True
    machA.loop = dummy_loop

    # Ensure fout has been open, initialize and loop have been called
    machA.start()
    assert machA.conman.has_initialized
    assert has_called_loop
    assert machA.fout != None
    machA.fout.close()

    # Reads the written output to make sure it's correct
    fin = open("output/A1.out", "r")
    assert fin.read()[:7] == "INIT,A,"
    fin.close()

def test_receive_message():
    """
    Tests that the receive_message function works
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()

    # If no messages to receive, short circuit to False
    assert machA.receive_message() == False

    machA.conman.msg_queue = Queue()
    machA.conman.msg_queue.put(Message(author="B", time=-1))
    machA.conman.msg_queue.put(Message(author="C", time=300))

    # Receive the first message
    assert machA.clock == 0
    assert machA.receive_message()
    assert machA.conman.msg_queue.qsize() == 1
    # Test that the logical clock time is bumped up by one
    # since the received message time is before current time
    assert machA.clock == 1

    # Receive the second message
    assert machA.receive_message()
    assert machA.conman.msg_queue.qsize() == 0
    # Test that the logical clock time is bumped up to one more
    # than the time of the message received
    assert machA.clock == 301

    # Try (and fail) to receive a third message
    assert machA.receive_message() == False

    # Reads the written output to make sure it's correct
    machA.fout.close()
    fin = open("output/A1.out", "r")
    lines = fin.readlines()
    assert lines[1][:12] == "RECEIVED,B,1"
    assert lines[2][:12] == "RECEIVED,C,0"
    fin.close()

def test_single_send():
    """
    Tests the validity of the to argument, and makes sure that
    the correct underlying conman function is called
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()

    # Test that you can only send to a valid (other) machine
    num_errors = 0
    try:
        machA.single_send("not real")
    except:
        num_errors += 1
    try:    
        machA.single_send("A")
    except:
        num_errors += 1
    try:
        machA.single_send("B")
    except:
        num_errors += 1
    assert num_errors == 2

    # Test that the conman send function was called
    assert machA.conman.sent == [("B", 0)]

    # Reads the written output to make sure it's correct
    machA.fout.close()
    fin = open("output/A1.out", "r")
    lines = fin.readlines()
    assert lines[1][:12] == "SINGLE_SEND,"
    fin.close()

def test_multi_send():
    """
    Tests that the multisend function hits the underline conman
    function twice, hitting each of the other machines
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()

    machA.multi_send()

    # Test that the conman send function was called
    assert machA.conman.sent == [("B", 0), ("C", 0)]

    # Reads the written output to make sure it's correct
    machA.fout.close()
    fin = open("output/A1.out", "r")
    lines = fin.readlines()
    assert lines[1][:11] == "MULTI_SEND,"
    fin.close()

def test_internal_event():
    """
    Tests that an internal event is properly logged
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()

    machA.internal_event()

    # Reads the written output to make sure it's correct
    machA.fout.close()
    fin = open("output/A1.out", "r")
    lines = fin.readlines()
    assert lines[1][:15] == "INTERNAL_EVENT,"
    fin.close()

def test_frame():
    """
    Tests that the frame function calls receive_message only when the
    msg_queue is not empty, and that it calls the correct send functions
    depending on the value of random.randint. Also tests that logical clock
    is updated properly
    """
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()

    # Count various function calls
    num_calls_to_receive_message = 0
    def dummy_receive_message():
        nonlocal num_calls_to_receive_message
        num_calls_to_receive_message += 1
        return True
    machA.receive_message = dummy_receive_message

    num_calls_to_single_send = 0
    def dummy_single_send(to):
        nonlocal num_calls_to_single_send
        num_calls_to_single_send += 1
    machA.single_send = dummy_single_send

    num_calls_to_multi_send = 0
    def dummy_multi_send():
        nonlocal num_calls_to_multi_send
        num_calls_to_multi_send += 1
    machA.multi_send = dummy_multi_send

    num_calls_to_internal_event = 0
    def dummy_internal_event():
        nonlocal num_calls_to_internal_event
        num_calls_to_internal_event += 1
    machA.internal_event = dummy_internal_event

    # Pre-load the queue
    machA.conman.msg_queue = Queue()
    machA.conman.msg_queue.put(Message(author="B", time=-1))
    machA.conman.msg_queue.put(Message(author="C", time=300))

    # Test that the receive_message function is called twice
    machA.frame()
    assert num_calls_to_receive_message == 1
    machA.frame()
    assert num_calls_to_receive_message == 2
    # Since we mocked out receive_message, the clock should still
    # be 0 and the queue should still have two messages
    assert machA.clock == 0
    assert machA.conman.msg_queue.qsize() == 2
    
    # Clean the queue
    machA.conman.msg_queue = Queue()

    # Test action one two times
    prime_randint(1)
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 1
    assert num_calls_to_multi_send == 0
    assert machA.clock == 1
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 2
    assert num_calls_to_multi_send == 0
    assert machA.clock == 2

    # Test action two two times
    prime_randint(2)
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 3
    assert num_calls_to_multi_send == 0
    assert machA.clock == 3
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 4
    assert num_calls_to_multi_send == 0
    assert machA.clock == 4

    # Test action three two times
    prime_randint(3)
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 4
    assert num_calls_to_multi_send == 1
    assert machA.clock == 5
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 4
    assert num_calls_to_multi_send == 2
    assert machA.clock == 6

    # Test everything else triggers internal event
    assert num_calls_to_internal_event == 0
    prime_randint(4)
    machA.frame()
    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 4
    assert num_calls_to_multi_send == 2
    assert num_calls_to_internal_event == 1
    assert machA.clock == 7

    prime_randint(5)
    machA.frame()
    prime_randint(6)
    machA.frame()
    prime_randint(7)
    machA.frame()
    prime_randint(8)
    machA.frame()
    prime_randint(9)
    machA.frame()
    prime_randint(10)
    machA.frame()

    assert num_calls_to_receive_message == 2
    assert num_calls_to_single_send == 4
    assert num_calls_to_multi_send == 2
    assert num_calls_to_internal_event == 7
    assert machA.clock == 13

def test_loop():
    """
    Tests that the loop function runs until time - start_time is greater than
    the experiment duration. Tests that on each iteration the frame function
    is called.
    """
    # Mock overload the get_time function
    old_get_time = consts.get_time
    old_duration = consts.EXPERIMENT_DURATION
    time_to_return = 0
    def dummy_get_time():
        nonlocal time_to_return
        return time_to_return
    consts.get_time = dummy_get_time
    consts.EXPERIMENT_DURATION = 60000

    # Set up the machine
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    # Mock the frame function to just increase time
    numFrames = 0
    def dummy_increment_time():
        nonlocal time_to_return
        nonlocal numFrames
        time_to_return += 1000
        numFrames += 1
    machA.frame = dummy_increment_time
    machA.loop()
    assert numFrames == 60
    consts.get_time = old_get_time
    consts.EXPERIMENT_DURATION = old_duration

def test_kill():
    """
    Tests that the kill function kills the machine. This means
    it needs to pass the kill call to the connectionmanager and
    close the log file.
    """
    # Starts the dummy machine 
    machA = Machine("A", 1, 0)
    machA.conman = MockedConnectionManager()
    machA.loop = lambda: None
    machA.start()
    
    # For overriding the log file close function
    has_closed_log = False
    def dummy_close():
        nonlocal has_closed_log
        has_closed_log = True
    machA.fout.close = dummy_close

    assert machA.conman.has_killed == False
    assert has_closed_log == False

    machA.kill()

    assert machA.conman.has_killed
    assert has_closed_log
