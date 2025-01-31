import os
import sys
import pandas as pd
import numpy as np

from scipy.stats import ks_2samp #check 2 different data smaple if there is data drift or not

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):

        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact

            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist:
                    is_found=False
                else:
                    is_found=True
                    status=False
                
                report.update({column:})

        except Exception as e:
            raise NetworkSecurityException
    

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #Read data from train and test
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

        except Exception as e:
            raise NetworkSecurityException(e,sys)