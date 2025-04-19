# metoffice_wow_feeder
Python scripts to push WeatherUnderground API data to Met Office UK/Ireland WOW (Weather Observations Website)

You will need to install additional Pythoin Modules:
- requests
- logging
- cv2
- numpy

You will also need to replace some parameters in both scripts:

metoffice_weather.py:
- PATH_TO_LOG

weather_getter_net.py:
- STATION_ID & API_KEY in https://api.weather.com/v2/pws/observations/current?stationId=STATION_ID&format=json&units=m&apiKey=API_KEY
- SITE_ID & SITE_KEY in http://wow.metoffice.gov.uk/automaticreading?siteid=SITE_ID&siteAuthenticationKey=SITE_KEY&dateutc=

Signup for Weather Underground for compatible Weather Stations (Free): www.wunderground.com/signup
Signup for MetOffice WOW Site: https://wow.metoffice.gov.uk/
More informations on the Format used by MEt Office WOW for Data Upload: https://wow.metoffice.gov.uk/support/dataformats#dataFileUpload

What is WOW (Weather Observations Website)?

The 'Weather Observations Website' (WOW) reflects recent advances in technology and how weather observations can be made. At the same time, the growing world of social networking online makes it relatively easy for anyone to get involved and share their weather observations.

    The Met Office is helping to co-ordinate the growth of the weather observing community in the UK, by asking anyone to submit the observations they are taking. This can be done using all levels of equipment, so there are no cost restrictions.
