import os
from abc import ABC, abstractmethod
import threading
import queue
import time
import pandas as pd

from Logger import Logger

#This is a base class for all LogParsers
class LogParserBase(ABC):
    # on_parsed_data callback to notify LogParserManager that parsed data is available
    def __init__(self, parsed_data_available):
        #queue to put new log files' path to process them in separate thread
        self._log_file_queue = queue.Queue()
        self._parsed_data_available = parsed_data_available
        self._thread = None
        self._is_running=False

    def start(self):
        #start thread to process log files
        self._is_running=True
        self._thread = threading.Thread(target=self._process_files, daemon=True)
        self._thread.start()

    def stop(self):
       print(f"Stopping parser {self.__class__.__name__}...")
       self._is_running=False

       while self._thread.is_alive():
           time.sleep(2)
           print("_thread is_alive")
       
       self._thread = None
       print(f"Stopped parser {self.__class__.__name__}.")
        
    def new_file_available(self, file_path):
        self._log_file_queue.put(file_path)

    # processing files' thread method
    def _process_files(self):
        while self._is_running:
           try:
                file_path = self._log_file_queue.get(timeout=1)
           except queue.Empty:
               continue

           try:
                if not self._is_running:
                    break

                logger.log(f"Parsing {file_path}")

                df = self._parseLogFile(file_path)

                if not self._is_running:
                    break

                if df is not None and not df.empty:
                    self._parsed_data_available(df, file_path)
                logger.log(f"Parsing {file_path} finished, rows count: {len(df)}")

           except Exception as e:
                logger.log(f"Error processing log file: {e}")
                continue
           finally:
                self._log_file_queue.task_done()
        print("Worker thread exiting")

    @abstractmethod
    def _parseLogFile(self, file_path) -> pd.DataFrame:
        pass

    @property
    @abstractmethod
    def extension(self):
         pass

