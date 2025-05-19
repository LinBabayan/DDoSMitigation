import os
from abc import ABC, abstractmethod

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import joblib

from Logger import Logger
from Constants import Models
from Options import options

class RandomForestModelBase(ABC):
    def __init__(self):
        self._model_folder = options.models_folder
        os.makedirs(self._model_folder, exist_ok=True)
        self._is_running = False
 
    @abstractmethod
    def train_model(self, df):
      pass

    def start(self):
        self._is_running = True

    def stop(self):
        self._is_running = False

    def _generate_classifier_model(self, model_name, df, feature_columns, label_column):
        if not self._is_running:
            return

        X = df[feature_columns]
        y = df[label_column]

        if not self._is_running:
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if not self._is_running:
            return

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        if not self._is_running:
            return

        y_pred = model.predict(X_test)

        if not self._is_running:
            return

        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        if not self._is_running:
            return

        logger.training_metrics_log(f"{model_name} Attack Detection Model Metrics:")
        logger.training_metrics_log(f" Accuracy: {accuracy:.4f}")
        logger.training_metrics_log(f" F1 Score: {f1:.4f}")
        logger.training_metrics_log(f"Precision: {precision:.4f}")
        logger.training_metrics_log(f"   Recall: {recall:.4f}")

        if not self._is_running:
            return

        file_path = f"{self._model_folder}/{Models[model_name].value}"
        joblib.dump(model, file_path)
        logger.log(f"{model_name} model saved to: {file_path}")

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
            is_attack=('label', 'max'),
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