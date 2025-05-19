from abc import ABC, abstractmethod
from Options import options

class AnalizerBase(ABC):
    def __init__(self):
        self._model_folder = options.models_folder
        self._is_running = False

    def start(self):
        self._is_running = True
        self._volume_model = self._load_model(f"{self._model_folder}/{Models[_volume_based_model_name].value}")
        self._protocol_model = self._load_model(f"{self._model_folder}/{Models[_protocol_based_model_name].value}")

        if self._volume_model == None or self._protocol_model == None:
            self._volume_model = None
            self._protocol_model = None
            self._is_running = False

    def stop(self):
        self._is_running = False
        self._volume_model = None
        self._protocol_model = None

    def _load_model(file_path):
        if not os.path.exists(file_path):
            logger.log(f"Model file {file_path} does not exists")
            return None

        model = joblib.load(file_path_volume_model)
        return model

    def _aggregate_df(self, df, group_by_columns):
        if not self._is_running:
            return
 
        df['second'] = df['timestamp'].dt.floor('S')  # round to nearest second
        df['bits'] = df['length'] * 8                 # convert length (in bytes) to bits: bytes * 8

        if not self._is_running:
            return

        agg_df = df.groupby(group_by_columns).agg(
            pps=('length', 'count'),
            gbps=('bits', 'sum'),
            day_of_week=('timestamp', lambda x: x.iloc[0].dayofweek)
        ).reset_index()

        if not self._is_running:
            return

        agg_df['second_of_day'] = (
            agg_df['second'].dt.hour * 3600 +
            agg_df['second'].dt.minute * 60 +
            agg_df['second'].dt.second
        )
        agg_df['is_weekend'] = agg_df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        return agg_df

    @property
    @abstractmethod
    def _volume_based_model_name(self):
         pass

    @property
    @abstractmethod
    def _protocol_based_model_name(self):
         pass