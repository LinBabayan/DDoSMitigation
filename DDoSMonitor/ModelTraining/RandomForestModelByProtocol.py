from Logger import Logger
from Constants import Models
from .RandomForestModelBase import RandomForestModelBase

class RandomForestModelByProtocol(RandomForestModelBase):
    def train_model(self, df):
        logger.log("Training protocol-aware volume and packet models")

        agg_df = self._aggregate_df(df, group_by_columns=['second', 'protocol_number'])

        # Train Volume-Based Model
        self._generate_classifier_model(
            model_name=Models.VolumeBasedByProtocol.name,
            df=agg_df,
            feature_columns=['gbps', 'second_of_day', 'protocol_number', 'is_weekend'],
            label_column='is_attack'
        )

        # Train Protocol-Based Model
        self._generate_classifier_model(
            model_name=Models.ProtocolBasedByProtocol.name,
            df=agg_df,
            feature_columns=['pps', 'second_of_day', 'protocol_number', 'is_weekend'],
            label_column='is_attack'
        )


