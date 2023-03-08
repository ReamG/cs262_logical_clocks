import sys
sys.path.append("..")
from schema.identity import Identity
from schema.message import Message
from connection_manager import ConnectionManager
import socket
import threading
import time
import consts
import pytest
from threading import Thread

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
    manager = ConnectionManager(BLANK_IDENTITY)
    assert manager.identity == BLANK_IDENTITY
    assert manager.socket_map == {}
    assert manager.alive == True

def test_kill():
    """
    Tests that killing the connection manager updates the flag
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    manager.kill()
    assert manager.alive == False

def test_kill_close():
    """
    Tests that killing the connection manager closes all sockets
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    A_dum_sock = socket.socket(0, 0)
    B_dum_sock = socket.socket(0, 0)
    manager.socket_map = {
        "A": A_dum_sock,
        "B": B_dum_sock
    }
    manager.kill()
    assert A_dum_sock.has_closed == True
    assert B_dum_sock.has_closed == True

def test_consume():
    """
    Tests that the consume function works
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    A_dum_sock = socket.socket(0, 0)

    A_msg = Message(author="A", time=1)
    B_msg = Message(author="B", time=2)
    C_msg = Message(author="C", time=3)

    A_dum_sock.add_fake_send(A_msg)
    A_dum_sock.add_fake_send(B_msg)
    A_dum_sock.add_fake_send(C_msg)

    manager.socket_map = {
        "A": A_dum_sock
    }

    manager.consume(A_dum_sock, "T")

    assert A_dum_sock.has_closed == True
    assert manager.msg_queue.get() == A_msg
    assert manager.msg_queue.get() == B_msg
    assert manager.msg_queue.get() == C_msg

def test_consume_bad_message():
    """
    Tests that the consume function errors gracefully on
    bad messages
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    A_dum_sock = socket.socket(0, 0)

    A_dum_sock.add_fake_send("not a message")

    manager.socket_map = {
        "A": A_dum_sock
    }

    manager.consume(A_dum_sock, "T")

    assert A_dum_sock.has_closed == True
    assert manager.msg_queue.empty() == True

def test_handle_consumers():
    """
    Tests that the handle consumers function works
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    A_dum_sock = socket.socket(0, 0)
    B_dum_sock = socket.socket(0, 0)

    A_msg = Message(author="A", time=1)
    B_msg = Message(author="B", time=2)

    A_dum_sock.add_fake_send(A_msg)

    B_dum_sock.add_fake_send(B_msg)

    manager.socket_map = {
        "A": A_dum_sock,
        "B": B_dum_sock
    }

    manager.handle_consumers()
    
    # Give threads time to spawn and die
    time.sleep(0.5)
    assert A_dum_sock.has_closed == True
    assert B_dum_sock.has_closed == True
    assert manager.msg_queue.get() == A_msg
    assert manager.msg_queue.get() == B_msg

def test_handle_consumers_simple():
    """
    Tests that handle consumers with no sockets works
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    manager.handle_consumers()
    
    assert len(threading.enumerate()) == 1
    assert manager.msg_queue.empty() == True

def test_listen():
    """
    Tests that the listen function calls necessary socket
    functions and correctly handles receiving introduction message
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    manager.identity.num_listens = 3

    A_dum_sock = socket.socket(0, 0)
    A_dum_sock.set_fake_accept_names(["A", "B", "C"])

    manager.listen(A_dum_sock)

    assert A_dum_sock.binded_to == ("localhost", 50052)
    assert A_dum_sock.has_listened == True
    assert A_dum_sock.has_closed == True
    assert sorted(list(manager.socket_map.keys())) == ["A", "B", "C"]

def test_connect():
    """
    Tests that connect uses the right address info and introduces
    the right identity
    """
    manager1 = ConnectionManager(consts.IDENTITY_B)
    manager1.connect("A")
    sock1 = manager1.socket_map["A"]

    assert sock1 is not None
    assert sock1.connected_to == (consts.IDENTITY_A.host_ip, consts.IDENTITY_A.host_port)
    assert sock1.sent == ["B".encode()]
    
    manager2 = ConnectionManager(consts.IDENTITY_C)
    manager2.connect("A")
    sock2 = manager2.socket_map["A"]

    assert sock2 is not None
    assert sock2.connected_to == (consts.IDENTITY_A.host_ip, consts.IDENTITY_A.host_port)
    assert sock2.sent == ["C".encode()]

def test_connect_bad_name():
    """
    Tests that attempting to connect to a peer that's not in the
    identity map will raise an error
    """
    manager = ConnectionManager(consts.IDENTITY_B)
    with pytest.raises(Exception):
        manager.connect("D")

def test_handle_connections():
    """
    Test that the handle connections function calls
    connect on all connections specified in the identity
    """
    identity = Identity(
        name="T",
        host_ip="localhost",
        host_port=50052,
        num_listens=0,
        connections=["A", "B", "C"]
    )

    dummy_list = []
    def dummy_connect(name):
        nonlocal dummy_list
        dummy_list.append(name)

    manager = ConnectionManager(identity)
    manager.connect = dummy_connect

    manager.handle_connections()
    assert dummy_list == ["A", "B", "C"]

def test_handle_connections_error():
    """
    Test that when the connect function fails it will continue
    retrying once per second
    """
    identity = Identity(
        name="T",
        host_ip="localhost",
        host_port=50052,
        num_listens=0,
        connections=["A", "B", "C"]
    )

    dummy_list = []
    def dummy_connect_error(name):
        nonlocal dummy_list
        dummy_list.append(name)
        raise Exception("Connect failed")
    def dummy_connect(name):
        nonlocal dummy_list
        dummy_list.append(name)

    manager = ConnectionManager(identity)
    manager.connect = dummy_connect_error

    shadow_thread = Thread(target=manager.handle_connections)
    shadow_thread.start()

    time.sleep(2.5)
    assert dummy_list == ["A", "A", "A"]
    manager.connect = dummy_connect
    time.sleep(1)
    assert dummy_list == ["A", "A", "A", "A", "B", "C"]

def test_initialize():
    """
    Test that the initialize function calls listen and handle_connections
    in separate threads, joins both of them, and then calls handle_consumers
    """
    manager = ConnectionManager(BLANK_IDENTITY)

    has_called_listen = False
    has_called_handle_connections = False

    def mock_listen():
        nonlocal has_called_listen
        has_called_listen = True
    
    def mock_handle_connections():
        nonlocal has_called_handle_connections
        has_called_handle_connections = True

    manager.listen = mock_listen
    manager.handle_connections = mock_handle_connections

    manager.initialize()

    assert has_called_listen == True
    assert has_called_handle_connections == True

def test_send():
    """
    Test that the send function calls the send function on the
    correct socket, and the write message is encoded and sent
    over the socket
    """
    manager = ConnectionManager(BLANK_IDENTITY)
    A_dum_sock = socket.socket(0, 0)
    manager.socket_map = {
        "A": A_dum_sock
    }

    manager.send("not exist", 100)

    assert A_dum_sock.sent == []

    manager.send("A", 100)

    assert A_dum_sock.sent == [str(Message("T",100)).encode()]

if __name__ == "__main__":
    print("All tests passed!")