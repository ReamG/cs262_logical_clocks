class Message:
    def __init__(self, author: str, time: int):
        self.author = author
        self.time = time

    @staticmethod
    def from_string(rep: str):
        """
        Parses a string into a Message object
        """
        parts = rep.split("::")
        return Message(parts[0], int(parts[1]))

    def __str__(self):
        return f"{self.author}::{self.time}"
    
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Message) and self.author == obj.author and self.time == obj.time