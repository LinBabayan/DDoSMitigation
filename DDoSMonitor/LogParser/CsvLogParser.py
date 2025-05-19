import pandas as pd
from datetime import datetime

from .LogParserBase import LogParserBase
from Constants import ParsedDataColumnNames
from Logger import Logger

required_columns = {
                    ParsedDataColumnNames.column_time: "Time",
                    ParsedDataColumnNames.column_protocol_N: "Protocol_N",
                    ParsedDataColumnNames.column_protocol: "Protocol",
                    ParsedDataColumnNames.column_length: "Length",
                    ParsedDataColumnNames.column_src_ip: "Source",
                    ParsedDataColumnNames.column_dst_ip: "Destination"
                    }

class CsvLogParser(LogParserBase):
    def __init__(self, parsed_data_available):
        super().__init__(parsed_data_available)
        self._setColumnMapping(required_columns)

    @property
    def extension(self):
         return ".csv"

    def _capture_time_utc(self):
         return datetime.utcnow()

    def _setColumnMapping(self, required_columns):
        self._required_columns = required_columns

        self._rename_mapping = {}
        for target_column, original_column in self._required_columns.items():
            self._rename_mapping[original_column] = target_column

    def _parseLogFile(self, file_path):
        try:
           if not self._is_running:
               return None

           df = pd.read_csv(file_path)
           if ParsedDataColumnNames.column_time in df:
                time_column = ParsedDataColumnNames.column_time
           elif required_columns[ParsedDataColumnNames.column_time] in df:
              time_column = required_columns[ParsedDataColumnNames.column_time]
           else:
              raise Exception(f"No time column in {file_path}")

           #convert time column to datetime
           if pd.api.types.is_datetime64_any_dtype(df[time_column]):
               #nothing to do
               pass
           elif pd.api.types.is_numeric_dtype(df[time_column]):
               # convert float time (seconds) to datetime
               capture_time = self._capture_time_utc()
               df[time_column] = df[time_column].apply(lambda x: capture_time + pd.to_timedelta(x, unit='s'))
           
           elif pd.api.types.is_object_dtype(df[time_column]):
               try:
                   df[time_column] = pd.to_datetime(df[time_column])
               except Exception as e:
                   raise Exception(f"Failed to convert string in {time_column} to datetime: {e}")
           else:
               raise Exception(f"{time_column} column is neither dateTime nor float. Cannot convert it to datetime")

           if not self._is_running:
               return None

           # Keep only required columns
           drop_columns = []
           for column in df.columns:
                if column not in self._required_columns.values() and column not in self._required_columns.keys():
                    drop_columns.append(column)
           df = df.drop(drop_columns, errors="ignore")

           df.rename(columns=self._rename_mapping, inplace=True)

           if ParsedDataColumnNames.column_protocol_N not in df.columns:
                df['protocol_number'] = df[ParsedDataColumnNames.column_protocol].apply(lambda name: net_protocol.get_protocol_number(name))

           return df

        except Exception as e:
            logger.log(f"Error processing {file_path}: {e}")
            return None



