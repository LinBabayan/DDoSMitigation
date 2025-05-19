import pandas as pd
from datetime import datetime
from decimal import Decimal

from LogParser.CsvLogParser import CsvLogParser
from Constants import ParsedDataColumnNames
from Constants import net_protocol

class TrainingDataReader(CsvLogParser):
    def __init__(self):
        super().__init__(None)
        self._capture_time = datetime.utcnow()

        self._required_columns = {
                    ParsedDataColumnNames.column_time: "Time",
                    ParsedDataColumnNames.column_protocol_N: "Protocol_N",
                    ParsedDataColumnNames.column_protocol: "Protocol",
                    ParsedDataColumnNames.column_length: "Length",
                    ParsedDataColumnNames.column_src_ip: "Source",
                    ParsedDataColumnNames.column_dst_ip: "Destination",
                    "label": "label"
                    }

        self._setColumnMapping(self._required_columns)
       
    def parseData(self, file_path) -> pd.DataFrame:
        df = self._parseLogFile(file_path)
 
        return df

    def _capture_time_utc(self):
         return self._capture_time