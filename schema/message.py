class Message:
    """
    A class that represents a message passed between two machines during
    the course of our experiment. It's simply the name of who sent the
    message and the value of their logical clock.
    """

    def __init__(self, author: str, time: int):
        self.author = author
        self.time = time

    @staticmethod
    def from_string(rep: str):
        """
        Parses a string into a Message object. Used for unmarshalling after
        receiving data over the socket.
        NOTE: Given the simplicity of messages, it really is as simple as just
        splitting at the first :: and requiring that machine names not include
        the string "::"
        """
        parts = rep.split("::")
        return Message(parts[0], int(parts[1]))

    def __str__(self):
        """
        Turns a message object into a string. Used for marshalling before
        sending data over the socket.
        """
        return f"{self.author}::{self.time}"
    
    def __eq__(self, obj: object) -> bool:
        """
        Helper function for testing to determine whether messages are
        equivalent.
        """
        return isinstance(obj, Message) and self.author == obj.author and self.time == obj.time