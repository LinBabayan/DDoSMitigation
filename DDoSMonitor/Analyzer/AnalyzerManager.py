from EventsHandler import events_handler
from EventsHandler import EventName
from .AnalyzerCommon import AnalyzerCommon
from .AnalyzerByProtocol import AnalyzerByProtocol

class AnalyzerManager(object):
    def __init__(self):
        self.analyzer_common = AnalyzerCommon()
        self.analyzer_by_protocol = AnalyzerByProtocol()

        events_handler.subscribe(EventName.PARSED_DATA_AVAILABLE, self._on_parsed_data_available)
        self._is_running = False
 
    def start(self):
       self._is_running = True
       self.analyzer_common.start()
       self.analyzer_by_protocol.start()

    def stop(self):
        self.analyzer_common.stop()
        self.analyzer_by_protocol.stop()
        self._is_running = False

    def _on_parsed_data_available(self, payload):
        df = payload['df']
        src_path = payload['src_path']
        
        if not self._is_running:
            return

        self.analyzer_common.process(df, src_path)

        if not self._is_running:
            return

        self.analyzer_by_protocol.process(df, src_path)



