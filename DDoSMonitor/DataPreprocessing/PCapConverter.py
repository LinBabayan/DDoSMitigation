import os
import pandas as pd
from scapy.utils import RawPcapReader, PcapReader
from datetime import datetime, timezone
from decimal import Decimal
from scapy.all import IP, IPv6, TCP, UDP, ICMP
from scapy.all import IP, IPv6
import glob

from Constants import ParsedDataColumnNames
from Constants import net_protocol
from Options import options

datetime_format = "%Y%m%d_%H_%M_%S"

class PCapConverter(object):

    def parsePcapToCsv(self, file_path, output_files_path, output_file_name, packets_count, label_infos = None, skip_packets = None):
       try:
            packet_idx = 0
            output_files_count = 0
            data = []

            with PcapReader(file_path) as pcap_reader:
               for packet in pcap_reader:
                   packet_idx += 1
                   if packet_idx % 1000 == 0:
                        print (f"Processed {packet_idx}")

                   if skip_packets is not None and packet_idx < skip_packets:
                       if packet_idx % packets_count == 0:
                            output_files_count +=1
                            print (f"Skipped processing {packet_idx}")
                       continue
                    
                   try:
                        timestamp = packet.time 
                        seconds = int(timestamp) 
                        microseconds = int((timestamp - Decimal(seconds)) * 1_000_000) 

                        dtUTC = datetime.utcfromtimestamp(seconds).replace(microsecond=microseconds)                        
                       
                        (proto_num, proto_name, src_ip, dst_ip, src_port, dst_port) = net_protocol.get_proto_info(packet)
                    
                        if proto_num == 999 or proto_name == "Unknown":
                            print (f"Unknown packet={packet_idx}")

                        row = {
                                "packet#": packet_idx,
                                ParsedDataColumnNames.column_time: dtUTC,
                                ParsedDataColumnNames.column_protocol_N: proto_num,
                                ParsedDataColumnNames.column_protocol: proto_name,
                                ParsedDataColumnNames.column_length: len(packet),
                                ParsedDataColumnNames.column_src_ip: src_ip,
                                ParsedDataColumnNames.column_dst_ip: dst_ip,
                                ParsedDataColumnNames.column_src_port: src_port,
                                ParsedDataColumnNames.column_dst_port: dst_port,
                                "label": 0 #self._get_label(label_infos, dtUTC, src_ip, dst_ip, src_port, dst_port)
                            }

                        data.append(row)
                        if packet_idx % packets_count == 0:
                            print(f"Processed {packets_count} packets, last packet # {packet_idx}...")

                            output_files_count +=1
                            df = pd.DataFrame(data)
                            dt = data[0]['timestamp'].strftime(datetime_format)
                            filename = f"{output_files_path}\\{output_file_name}_{dt}.{output_files_count}.csv"

                            df.to_csv(filename, index=False)

                            data.clear()

                   except Exception as packet_error:
                        print(f"Error processing packet {packet_idx}: {packet_error}")
                        continue 
       except Exception as e:
            print(e)
            return None

    def _get_label(self, label_infos, dtUTC, src_ip, dst_ip, src_port, dst_port):
        if label_infos is None:
           return 0

        for label_info in label_infos:
            if (label_info['start_time'] is None or dtUTC >= label_info['start_time']) and \
               (label_info['end_time'] is None or dtUTC <= label_info['end_time']) and \
               (label_info['src_ip'] is None or src_ip == label_info['src_ip']) and \
               (label_info['dst_ip'] is None or dst_ip == label_info.get('dst_ip')):
                return 1

        return 0
    
if __name__ == "__main__":
    converter = PCapConverter()
    output_files_path = options.train_data_folder
    os.makedirs(output_files_path, exist_ok=True)

    #file = "TrainingData\\downloads\\Monday-WorkingHours.pcap"
    #df = converter.parsePcapToCsv(file, output_files_path, "1_Monday", 100000)
    
    #file = "TrainingData\\downloads\\Tuesday-WorkingHours.pcap"
    #df = converter.parsePcapToCsv(file, output_files_path, "2_Tuesday", 100000)

    #file = "TrainingData\\downloads\\Wednesday-workingHours.pcap"
    #df = converter.parsePcapToCsv(file, output_files_path, "3_Wednesday", 100000)
  
    file = "TrainingData\\downloads\\Thursday-WorkingHours.pcap"
    df = converter.parsePcapToCsv(file, output_files_path, "4_Thursday", 100000)
    
    #file = "TrainingData\\downloads\\Friday-WorkingHours.pcap"
    #df = converter.parsePcapToCsv(file, output_files_path, "5_Friday", 100000)


