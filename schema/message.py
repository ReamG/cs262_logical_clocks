class Message:
    def __init__(self, author: str, message: str):
        self.author = author
        self.message = message

    @staticmethod
    def from_string(rep: str):
        """
        Parses a string into a Message object
        """
        parts = rep.split("::")
        return Message(parts[0], parts[1])

    def __str__(self):
        return f"{self.author}::{self.message}"
    
    def __eq__(self, obj: object) -> bool:
        return isinstance(obj, Message) and self.author == obj.author and self.message == obj.message