from datetime import datetime
from scapy.utils import PcapReader
from scapy.all import IP, IPv6, TCP, UDP, ICMP
from scapy.all import IP, IPv6
import pandas as pd
from datetime import datetime

from Constants import ParsedDataColumnNames
from Constants import net_protocol
from .LogParserBase import LogParserBase
from Logger import Logger

class PCapLogParser(LogParserBase):
    def __init__(self, parsed_data_available):
        super().__init__(parsed_data_available)

    @property
    def extension(self):
            return ".pcap"

    def _parseLogFile(self, file_path):
        try:
            if not self._is_running:
                return None

            data = []
            i = 0

            with PcapReader(file_path) as pcap_reader:
                for packet in pcap_reader:
                    if not self._is_running:
                        return None

                    try:
                        timestamp = packet.time 
                        seconds = int(timestamp) 
                        microseconds = int((timestamp - Decimal(seconds)) * 1_000_000) 

                        dtUTC = datetime.utcfromtimestamp(seconds).replace(microsecond=microseconds)                        
                       
                        (proto_num, proto_name, src_ip, dst_ip, src_port, dst_port) = net_protocol.get_proto_info(packet)

                        row = {
                            ParsedDataColumnNames.column_time: dtUTC,
                            ParsedDataColumnNames.column_protocol_N: proto_num,
                            ParsedDataColumnNames.column_protocol: proto_name,
                            ParsedDataColumnNames.column_length: len(packet),
                            ParsedDataColumnNames.column_src_ip: src_ip,
                            ParsedDataColumnNames.column_dst_ip: dst_ip,
                            ParsedDataColumnNames.column_src_port: src_port,
                            ParsedDataColumnNames.column_dst_port: dst_port
                        }

                        data.append(row)
                        i += 1
                        if i % 1000 == 0:
                            print(f"Processed {i} packets...")

                    except Exception as packet_error:
                        print(f"Error processing packet {i}: {packet_error}")
                        continue 

            df = pd.DataFrame(data)
            return df

        except Exception as e:
            print(e)
            Logger.log(f"Error processing {file_path} on row = {len(data)}: {e}")
            return None

