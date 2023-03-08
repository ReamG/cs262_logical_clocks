import time
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

# Helper function to get systemtime in milliseconds
def get_time() -> int:
    return int(round(time.time() * 1000))

# Helper function to get a list of other machines
def get_other_machines(name: str) -> list[str]:
    return [key for key in IDENTITY_MAP.keys() if key != name]

EXPERIMENT_DURATION = 66000 # In milliseconds