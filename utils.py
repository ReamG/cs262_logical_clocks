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

# NOTE: found at https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()