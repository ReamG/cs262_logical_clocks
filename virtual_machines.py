import socket
import time
import numpy as np

class vm():

    def __init__(self, rate, port):
        self.log = []
        self.rate = rate
        self.port = port


    def start(self):
        while True:
            time.sleep(1/self.rate)
            op_code = np.random.randint(1,11)

            if op_code == 1:
                pass
            elif op_code == 2:
                pass
            elif op_code == 3:
                pass
            else:
                pass