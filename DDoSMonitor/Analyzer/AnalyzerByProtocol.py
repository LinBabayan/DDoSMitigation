import pandas as pd
import joblib
from datetime import datetime

from Constants import Models
from Logger import Logger
from .AnalizerBase import AnalizerBase

class AnalyzerByProtocol(AnalizerBase):
    def __init__(self):
        super().__init__()

    def process(self, df, src_path):
        if not self._is_running:
            return

        try:
            _aggregate_df(df, group_by_columns=['second'])
            if not self._is_running:
                return

            X_volume = agg_df[['second_of_day', 'is_weekend', 'gbps']]
            X_protocol = agg_df[['second_of_day', 'is_weekend', 'pps']]
            if not self._is_running:
                return

            # Predict attacks
            volume_predictions = self._volume_protocol_analisis_model.predict(X_volume)
            protocol_predictions = self._packet_protocol_analysis_model.predict(X_protocol)
            if not self._is_running:
                return

            # Handle predictions
            attack_detected = False
            for second, protocol_number, volume_pred, packet_pred in zip(agg_df['second'], agg_df['protocol_number'], volume_predictions, packet_predictions):
                protocol_name = net_protocol.get_protocol_name(protocol_number) 

                if vol_pred == 1:
                    Logger.status_log(f"[VolumeBased] {protocol_name} flood detected at {second.strftime('%Y-%m-%d %H:%M:%S')} | Source: {src_path}", is_attack=True)
                    attack_detected = True
                if proto_pred == 1:
                    Logger.status_log(f"[ProtocolBased] {protocol_name} flood detected at {second.strftime('%Y-%m-%d %H:%M:%S')} | Source: {src_path}", is_attack=True)
                    attack_detected = True

            if not attack_detected:
                Logger.status_log(f"No protocol flood detected | Source: {src_path}", is_attack=False)

        except Exception as e:
            Logger.log(f"Error analyzing by protocol {file_path}: {e}")
            return None

    @property
    def _volume_based_model_name(self):
        return Models.VolumeBasedByProtocol

    @property
    def _protocol_based_model_name(self):
        return Models.ProtocolBasedByProtocol

