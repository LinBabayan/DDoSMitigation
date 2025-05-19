from Logger import logger
from Constants import Models
from .RandomForestModelBase import RandomForestModelBase

class RandomForestModelCommon(RandomForestModelBase):
    def train_model(self, df):
        logger.log("Training common volume and protocol models")

        agg_df = self._aggregate_df(df, group_by_columns=['second'])

        # Train Volume-Based Model
        self._generate_classifier_model(
            model_name=Models.VolumeBased.name,
            df=agg_df,
            feature_columns=['gbps', 'second_of_day', 'is_weekend'],
            label_column='is_attack'
        )

        # Train Protocol-Based Model
        self._generate_classifier_model(
            model_name=Models.ProtocolBased.name,
            df=agg_df,
            feature_columns=['pps', 'second_of_day', 'is_weekend'],
            label_column='is_attack'
        )
