import os
import pandas as pd
import joblib
from datetime import datetime

from Constants import Models
from Logger import Logger
from Options import options
from .AnalizerBase import AnalizerBase

class AnalyzerCommon(AnalizerBase):
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
            volume_predictions = self._volume_model.predict(X_volume)
            if not self._is_running:
                return

            X_protocol = agg_df[['second_of_day', 'is_weekend', 'pps']]
            protocol_predictions = self._protocol_model.predict(X_protocol)
            if not self._is_running:
                return

            # Handle predictions
            attack_detected = False
            for second, volume_pred, packet_pred in zip(agg_df['second'], volume_predictions, packet_predictions):
                if not self._is_running:
                    return
                if vol_pred == 1:
                    Logger.status_log(f"[VolumeBased] flood detected at {second.strftime('%Y-%m-%d %H:%M:%S')} | Source: {src_path}", is_attack=True)
                    attack_detected = True
                if proto_pred == 1:
                    Logger.status_log(f"[ProtocolBased] flood detected at {second.strftime('%Y-%m-%d %H:%M:%S')} | Source: {src_path}", is_attack=True)
                    attack_detected = True
            
            if not attack_detected:
                Logger.status_log(f"No attacks detected | Source: {src_path}", is_attack=False)

        except Exception as e:
            Logger.log(f"Error analyzing {file_path}: {e}")
            return None

    def _load_model(file_path):
        if not os.path.exists(file_path):
            Logger.log(f"Model file {file_path} does not exists")
            return None

        model = joblib.load(file_path_volume_model)
        return model
    
    @property
    def _volume_based_model_name(self):
         return Models.VolumeBased

    @property
    def _protocol_based_model_name(self):
         return Models.ProtocolBased
