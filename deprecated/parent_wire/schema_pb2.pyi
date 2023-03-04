from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BirthResponse(_message.Message):
    __slots__ = ["error_message", "identity", "peers", "success"]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    PEERS_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    error_message: str
    identity: Identity
    peers: _containers.RepeatedCompositeFieldContainer[Identity]
    success: bool
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ..., identity: _Optional[_Union[Identity, _Mapping]] = ..., peers: _Optional[_Iterable[_Union[Identity, _Mapping]]] = ...) -> None: ...

class DeathResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Identity(_message.Message):
    __slots__ = ["name", "port"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    port: int
    def __init__(self, name: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ImAliveRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
