# File in : 
# PATH_TO_LOG

import os
import time
import logging
import requests
from logging.handlers import RotatingFileHandler
import cv2
import numpy as np

from weather_getter_met import WeatherGetterMet

class WeatherBot():

    def __init__(self):
        self.wg = WeatherGetterMet()

    def run(self):
        """Run the application"""
        # Get the current weather
        self.wg.get_weather()

if __name__ =="__main__":
    handlers = [ RotatingFileHandler(filename='/PATH_TO_LOG/data.log', 
                mode='w', 
                maxBytes=512000, 
                backupCount=4)
               ]
    logging.basicConfig(handlers=handlers, 
                        level=logging.DEBUG, 
                        format='%(levelname)s %(asctime)s %(lineno)d %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')
         
    logger = logging.getLogger('my_logger')

    wtb = WeatherBot()
    wtb.run()
