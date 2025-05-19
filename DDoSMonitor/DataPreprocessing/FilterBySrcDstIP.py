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

class FilterBySrcDstIP(object):
    def filterData(self, file, output_file_path):
        df = pd.DataFrame()
        try:
            for file in files:
                df_file = pd.read_csv(file)
                df_file['timestamp'] = pd.to_datetime(df_file['timestamp'], utc=True, errors='coerce')
                df_file['second'] = df_file['timestamp'].dt.floor('S')  
                df_file['bits'] = df_file['length'] * 8                 

                filtered_df = df_file[df_file['src_ip'].isin([
                    "192.168.10.3",   # Kali
                    # "192.168.10.14",  # Win bot
                    # "192.168.10.15",  # Win bot
                    # "192.168.10.9"    # Win bot
                ])]
                df = pd.concat([df, filtered_df], ignore_index=True)
                print(f"Processed {file}")

            agg_df = df.groupby(['second', 'src_ip']).agg(
                    pps=('length', 'count'),
                    gbps=('bits', 'sum')
                ).reset_index()

            agg_df['second'] = agg_df['second'].dt.strftime('%H:%M:%S')
            agg_df.to_csv(f"{output_file_path}_filtered_agg.csv", index=False)

            df['second'] = df['second'].dt.strftime('%H:%M:%S')
            df.to_csv(f"{output_file_path}_filtered.csv", index=False)

        except Exception as e:
            print(e)
            return None

if __name__ == "__main__":
    files = []
    files.extend(glob.glob(os.path.join(options.train_data_folder, "3_Wednesday*.csv")))
    output_path = f"{options.train_data_folder}\\Agg\\Filtered\\Wednesday"
    os.makedirs(f"{options.train_data_folder}\\Agg\\Filtered\\", exist_ok=True)


    processor = FilterBySrcDstIP()
    processor.filterData(files, output_path)

