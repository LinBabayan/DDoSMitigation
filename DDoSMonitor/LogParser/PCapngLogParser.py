from datetime import datetime
from scapy.all import rdpcap, IP, IPv6, TCP, UDP, ICMP
import pandas as pd

from .PCapLogParser import PCapLogParser

class PCapngLogParser(PCapLogParser):
    def __init__(self, parsed_data_available_callback):
        super().__init__(parsed_data_available_callback)

    @property
    def extension(self):
        return ".pcapng"
