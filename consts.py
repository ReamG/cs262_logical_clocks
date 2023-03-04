from typing import Mapping
from schema.identity import Identity

# Create the three identities that the machines can assume
IDENTITY_A = Identity(
    name="A",
    host_ip="localhost",
    host_port=50051,
    num_listens=2,
    connections=[]
)

IDENTITY_B = Identity(
    name="B",
    host_ip="localhost",
    host_port=50052,
    num_listens=1,
    connections=["A"]
)

IDENTITY_C = Identity(
    name="C",
    host_ip="localhost",
    host_port=50053,
    num_listens=0,
    connections=["A", "B"],
)

# Create a mapping from identity name to information about it
IDENTITY_MAP: Mapping[str, Identity] = {
    "A": IDENTITY_A,
    "B": IDENTITY_B,
    "C": IDENTITY_C,
}
