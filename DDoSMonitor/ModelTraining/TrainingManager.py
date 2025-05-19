import os
import pandas as pd
import glob
import numpy as np
import threading
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

from Options import options
from Logger import logger
from EventsHandler import events_handler

from ModelTraining.TrainingDataReader import TrainingDataReader
from ModelTraining.RandomForestModelCommon import RandomForestModelCommon
from ModelTraining.RandomForestModelByProtocol import RandomForestModelByProtocol

class TrainingManager:
    def __init__(self):
        self._train_data_folder = options.train_data_folder
        
        self._train_data_reader = TrainingDataReader()
        self._random_forest_model_common = RandomForestModelCommon()
        self._random_forest_model_by_protocol = RandomForestModelByProtocol()
        
        self._is_running = False

    def start(self):
        self._is_running = True
        self._train_data_reader.start()
        self._random_forest_model_common.start()
        self._random_forest_model_by_protocol.start()

        #create model in separate thread
        self._training_thread = threading.Thread(target=self.create_model)
        self._training_thread.start()

    def stop(self):
        self._is_running = False

        self._train_data_reader.stop()
        self._random_forest_model_common.stop()
        self._random_forest_model_by_protocol.stop()

        if self._training_thread is not None:
            while self._training_thread.is_alive():
               time.sleep(2)
               print("_training_thread is_alive")
       
        self._training_thread = None

    def create_model(self):
        try:
            csv_files = []
            csv_files.extend(glob.glob(os.path.join(self._train_data_folder, "*.csv")))

            if len(csv_files) == 0:
                logger.log(f"No *.csv files in {self._train_data_folder}, model training skipped!", is_error=True)
                self._is_running = False
                return

            csv_files.sort()

            print(f"self._is_running 2 = {self._is_running}")

            logger.log(f"Loading training data, files count={len(csv_files)}")

            print(f"self._is_running 3 = {self._is_running}")

            self._df = pd.DataFrame()
            for file in csv_files:
                if not self._is_running:
                    break

                logger.log(f"Parsing {file}")
                df_file = self._train_data_reader.parseData(file)

                if not self._is_running:
                    break
                if df_file is None:
                    continue

                self._df = pd.concat([self._df, df_file], ignore_index=True)
                logger.log(f"Parsing {file} finished, rows count: {len(self._df)}")
        
            if not self._is_running:
                return

            logger.log(f"Loading training data finished, rows count: {len(self._df)}")

            logger.log(f"Training models started")
            self._random_forest_model_common.train_model(self._df)
        
            if not self._is_running:
                return

            self._random_forest_model_by_protocol.train_model(df)
        
            self._is_running = False
            logger.log(f"Training models finished")
        
            events_handler.publish(EventName.TRAINING_MODEL_FINISHED)

        except Exception as e:
            logger.log(f"Error training model: {e}")
            self._is_running = False
            return None       

