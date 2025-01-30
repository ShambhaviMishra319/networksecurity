import yaml

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file: ##Opens the YAML file in binary read mode ("rb"), meaning it reads the file as bytes instead of a string.
            return yaml.safe_load(yaml_file)  #Parses it safely into a dictionary
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e