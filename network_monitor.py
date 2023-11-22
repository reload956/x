import psutil
import time
from enum import Enum
import threading
import time

class States(Enum):
    Offline: 0 # no networks detected
    Unset: 1 # not connected to any network
    Connected: 2 # connected

class Network:

    state = States.Offline

    def __init__(self) -> None:
        thread = threading.Thread(target=check_network)  
        thread.start()

def check_network(self):
    while True:        
        try:
            # Get list of network interfaces
            ifaces = psutil.net_if_addrs()  

            # Check if list is empty
            if not ifaces:
                self.state = States.Unset
            else:
                self.state = States.Connected
        except Exception:
            self.state = States.Offline
        
        time.sleep(5)

def monitor_network(self, intervals):
    if not self.state == States.Connected:
        return
    tot_sent = 0
    tot_recv = 0
    for interval in range(intervals):
        bytes_sent = psutil.net_io_counters().bytes_sent 
        bytes_recv = psutil.net_io_counters().bytes_recv

        sent_per_sec = (bytes_sent - tot_sent) / 1024 / 1024 # MB 
        recv_per_sec = (bytes_recv - tot_recv) / 1024 / 1024 

        print(f"Sent: {sent_per_sec:.2f} MB | Received: {recv_per_sec:.2f} MB")

        tot_sent = bytes_sent
        tot_recv = bytes_recv
        
        time.sleep(1)