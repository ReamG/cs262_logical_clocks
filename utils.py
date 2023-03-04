# Helper functions used throughout machine and sub-components

def print_error(msg: str):
    """
    Prints an error message in red
    """
    print(f"\033[91mERROR: {msg}\033[0m")

def print_warning(msg: str):
    """
    Prints a warning message in yellow
    """
    print(f"\033[93mWARNING: {msg}\033[0m")

def print_success(msg: str):
    """
    Prints a success message in green
    """
    print(f"\033[92mSUCCESS: {msg}\033[0m")

def print_info(msg: str):
    """
    Prints an info message in blue
    """
    print(f"\033[94mINFO: {msg}\033[0m")