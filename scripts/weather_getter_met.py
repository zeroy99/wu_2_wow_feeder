#!/usr/bin/env python3

# wu_2_wow_feeder by ZeRoY - April 2025
# Wunderground API - Replace:
# STATION_ID & API_KEY in https://api.weather.com/v2/pws/observations/current?stationId=STATION_ID&format=json&units=m&apiKey=API_KEY
# 
# Met Office Data - Replace:
# SITE_ID & SITE_KEY in http://wow.metoffice.gov.uk/automaticreading?siteid=SITE_ID&siteAuthenticationKey=SITE_KEY&dateutc=

import os
import logging
import requests
import datetime

class WeatherGetterMet():
    """Class for retrieving the weather"""

    def __init__(self):
        """Set up the class"""
    
    def _get_weather_from_api(self):
        """Returns the response from the weather api"""
        logging.info('Retrieving weather from API')
        response = requests.get('https://api.weather.com/v2/pws/observations/current?stationId=STATION_ID&format=json&units=m&apiKey=API_KEY')
        if response.status_code == 200:
            return response.json()

    def _get_humidity(self):
        """Returns the temperature"""
        return (self.wx['observations'][0]['humidity'])

    def _get_temp(self):
        """Returns the temperature"""
        return (self.wx['observations'][0]['metric']['temp'])

    def _get_windspeed(self):
        """Returns the Wind Speed"""
        self.windspeed = (self.wx['observations'][0]['metric']['windSpeed'])
        return self.convert_speed(self.windspeed)

    def _get_pressure(self):
        """Returns the Pressure"""
        self.pressure_float = (self.wx['observations'][0]['metric']['pressure'])
        self.pressure_limited_float = round(self.pressure_float, 2)
        return self.pressure_limited_float

    def _get_rain(self):
        """Returns the Precipitation last hour"""
        return (self.wx['observations'][0]['metric']['precipRate'])

    def _get_rain_24h(self):
        """Returns the Precipitation last 24h"""
        return (self.wx['observations'][0]['metric']['precipTotal'])

    def _get_dewpt(self):
        """Returns the Dew Point"""
        return (self.wx['observations'][0]['metric']['dewpt'])

    def _get_windchill(self):
        """Returns the WindChill"""
        return (self.wx['observations'][0]['metric']['windChill'])

    def _get_windgust(self):
        """Returns the Wind Gust"""
        self.windgust = (self.wx['observations'][0]['metric']['windGust'])
        return self.convert_speed(self.windgust)

    def _get_winddir_int(self):
        """Returns the Wind Direction INT"""
        return (self.wx['observations'][0]['winddir'])

    def _get_winddir(self):
        """Returns the Wind Direction ENGLISH"""
        self.winddir =  round(int(self.wx['observations'][0]['winddir']))
        return self.degToCompass(self.winddir)

    def _get_weather_desc2(self):
        """Returns weather Station Name"""
        return self.wx['observations'][0]['obsTimeUtc']

    def _get_weather_desc(self):
        """Returns weather Station Name"""
        return self.wx['observations'][0]['obsTimeLocal']

    def _get_uvindex(self):
        """Returns weather Station Name"""
        return self.wx['observations'][0]['uv']

    def degToCompass(self, num):
        val=int((num/22.5)+.5)
        arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        return arr[(val % 16)]

    # given epoch time 
    def _get_epoch(self):
        self.epoch = self.wx['observations'][0]['epoch']
        return self.convert_epoch(self.epoch)

    def convert_epoch(self, num):
        # given epoch time  
        epoch_time = num          
        # using datetime.fromtimestamp() function to convert epoch time into datetime object  
        mytimestamp = datetime.datetime.fromtimestamp( epoch_time )          
        # using strftime() function to convert  
        datetime_str = mytimestamp.strftime("%Y-%m-%d %H:%M:%S")
        return datetime_str

    def convert_speed(self, num):
        # function to convert speed from source km/h to miles/h
        return (0.621371* num)

    def get_weather(self):
        """Gets the weather from remote and sets class properties"""
        self.wx = self._get_weather_from_api()
        logging.debug(self.wx)
        self.description = self._get_weather_desc()
        logging.debug(self.description)
        self.description2 = self._get_weather_desc2()
        logging.debug(self.description2)
        self.humidity = self._get_humidity()
        logging.debug(self.humidity)
        self.temp = self._get_temp()
        logging.debug(self.temp)
        self.windspeed = self._get_windspeed()
        logging.debug(self.windspeed)
        self.pressure = self._get_pressure()
        logging.debug(self.pressure)
        self.rain = self._get_rain()
        logging.debug(self.rain)
        self.rain24h = self._get_rain_24h()
        logging.debug(self.rain24h)
        self.winddir = self._get_winddir()
        logging.debug(self.winddir)
        self.winddir_int = self._get_winddir_int()
        logging.debug(self.winddir_int)
        self.dewpt = self._get_dewpt()
        logging.debug(self.dewpt)
        self.windchill = self._get_windchill()
        logging.debug(self.windchill)
        self.windgust = self._get_windgust()
        logging.debug(self.windgust)
        self.epoch = self._get_epoch()
        logging.debug(self.epoch)
        self.uvindex = self._get_uvindex()
        logging.debug(self.uvindex)

        self.write_data = self.write_data(self.epoch,self.description2,self.description,self.humidity,self.temp,self.windspeed,self.pressure,self.rain,self.rain24h,self.winddir_int,self.winddir,self.dewpt,self.windchill,self.windgust,self.uvindex)

    def write_data(self,epoch,date_utc,date,humidity,temp,windspeed,pressure,rain,rain24h,winddir_int,winddir,dewpt,windchill,windgust,uvindex):
        # Some data conversion to suit WOW MET.CO.UK

        d = datetime.datetime.strptime(date, "%Y-%m-%d  %H:%M:%S")

        tempf = (temp * 1.8) + 32
        dewptf = (dewpt * 1.8) + 32

        date_result = epoch #Change for WOW Always needing UTC
        # Replace ':' with '%3A'
        date_result = date_result.replace(":", "%3A")
        # Replace spaces with '+'
        date_result = date_result.replace(" ", "+")

        # Air pressure in millibars (hPa)
        pressure_mb = pressure
        # Conversion factor
        mb_to_inhg = 0.02953
        # Convert to inches of mercury
        pressure_inhg = pressure_mb * mb_to_inhg
        
        # Rain from mm to inches
        rain_in = rain / 25.4
        rain_daily = rain24h / 25.4

        url = 'http://wow.metoffice.gov.uk/automaticreading?siteid=SITE_ID&siteAuthenticationKey=SITE_KEY&dateutc='+str(date_result)+'&winddir='+str(winddir_int)+'&windspeedmph='+str(windspeed)+'&windgustmph='+str(windgust)+'&humidity='+str(humidity)+'&tempf='+str(tempf)+'&rainin='+str(rain_in)+'&dailyrainin='+str(rain_daily)+'&baromin='+str(pressure_inhg)+'&dewptf='+str(dewptf)+'&UV='+str(uvindex)+'&softwaretype=CustomPython&action=updateraw'

        response = requests.post( url )
        if (response.status_code >= 200) and (response.status_code <= 299):
            json_response_str = response.content.decode('utf8').replace("'", '"')
            logging.debug("wow response: " + json_response_str )
        else:
            logging.debug(" %%%% wow reporting failure status: " + str(response.status_code) + " reason: " + response.reason )