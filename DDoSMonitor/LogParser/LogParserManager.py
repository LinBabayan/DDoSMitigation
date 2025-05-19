import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd

from .PCapngLogParser import PCapngLogParser
from .PCapLogParser import PCapLogParser
from .CsvLogParser import CsvLogParser

from EventsHandler import events_handler
from EventsHandler import EventName
from Options import options

class LogParserManager(FileSystemEventHandler):
    def __init__ (self):
        self._parsers = {
            CsvLogParser(self._on_parsed_data_available),
            PCapLogParser(self._on_parsed_data_available),
            PCapngLogParser(self._on_parsed_data_available)
            }
       
        self._log_folders = options.realtime_data_folders

        self._observer = Observer()
        self._is_running = False

    def start(self):
       for folder in self._log_folders:
            self._observer.schedule(self, folder, recursive=False)
       self._observer.start()

       self._is_running = True

       for parser in self._parsers:
            parser.start()

    def stop(self):
        if self._is_running:   
            self._observer.stop()
            self._observer.join()
        self._is_running = False

        for parser in self._parsers:
            parser.stop()

    def on_created(self, event):
        if event.is_directory:
            return
 
        #dispatch file to appropriate parser based on extension
        _, ext = os.path.splitext(event.src_path)
        for parser in self._parsers:
            if not self._is_running:
                break

            if ext.lower() == parser.extension:
                parser.new_file_available(event.src_path)
                break

    def _on_parsed_data_available(self, df, src_path):
        if df is not None and not df.empty and self._is_running:
            events_handler.publish(EventName.PARSED_DATA_AVAILABLE,  {'df': df, 'src_path': src_path})

        
        
        




