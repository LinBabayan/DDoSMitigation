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

class AggregationBySecond(object):
   def aggregateParsedData(self, files, output_file_path):
       try:
           df = pd.DataFrame()

           for file in files:
                df_file = pd.read_csv(file)
                df_file['timestamp'] = pd.to_datetime(df_file['timestamp'], utc=True, errors='coerce')
                df_file['second'] = df_file['timestamp'].dt.floor('S')  
                df_file['bits'] = df_file['length'] * 8                 

                df = pd.concat([df, df_file], ignore_index=True)
           
                print(f"Processed {file}")

           print(f"Processing total {len(df)}")
         
           agg_df = df.groupby(['second']).agg(
                gbps=('bits', 'sum')
            ).reset_index()

           agg_df['second'] = agg_df['second'].dt.strftime('%H:%M:%S')
           agg_df.to_csv(f"{output_file_path}", index=False)

       except Exception as e:
            print(e)
            return None


if __name__ == "__main__":
    files = []
    #files.extend(glob.glob(os.path.join(options.train_data_folder, "1_Monday*.csv")))
    #output_path = f"{options.train_data_folder}Agg\\AggregateBySec\\Monday_agg_by_sec_.csv"
    #os.makedirs(f"{options.train_data_folder}Agg\\AggregateBySec\\", exist_ok=True)

    files.extend(glob.glob(os.path.join(options.train_data_folder, "2_Tuesday*.csv")))
    output_path = f"{options.train_data_folder}Agg\\AggregateBySec\\Tuesday_agg_by_sec.csv"
    os.makedirs(f"{options.train_data_folder}Agg\\AggregateBySec\\", exist_ok=True)

    #files.extend(glob.glob(os.path.join(options.train_data_folder, "3_Wednesday*.csv")))
    #output_path = f"{options.train_data_folder}Agg\\AggregateBySec\\Wednesday_agg_by_sec.csv"
    #os.makedirs(f"{options.train_data_folder}Agg\\AggregateBySec\\", exist_ok=True)

    #files.extend(glob.glob(os.path.join(options.train_data_folder, "4_Thursday*.csv")))
    #output_path = f"{options.train_data_folder}Agg\\AggregateBySec\\Thursday_agg_by_sec.csv"
    #os.makedirs(f"{options.train_data_folder}Agg\\AggregateBySec\\", exist_ok=True)

    #files.extend(glob.glob(os.path.join(options.train_data_folder, "5_Friday*.csv")))
    #output_path = f"{options.train_data_folder}Agg\\AggregateBySec\\Friday_agg_by_sec.csv"
    #os.makedirs(f"{options.train_data_folder}Agg\\AggregateBySec\\", exist_ok=True)

    processor = AggregationBySecond()
    processor.aggregateParsedData(files, output_path)




