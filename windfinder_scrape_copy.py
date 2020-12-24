import json
import time

import requests
from bs4 import BeautifulSoup

from operators import decode_weather, convert_super_lists_to_24_average, convert_super_lists_to_24_without_average, \
    combine_normal_and_superforecast, is_superforecast_available
from scraping_tools import get_day_lists, get_temperature_list, get_cooridnates
from scraping_tools import get_wind_and_gusts_list, get_hours_list, get_wind_direction_list, \
    get_weather_and_day_list, get_rain_list, get_wave_height_list, get_wave_period_list, get_wave_direction_list, \
    get_day_lists_super, get_temperature_list_super, get_current_wind_and_is_weather_station
from spot_lists import get_spot_lists
from write_to_json import write_to_json
from savesh import savesh

#measure time for websites loading, calculating, saving
"""total_web = 0
total_exec = 0
total_save = 0

json_file = []
#import and separate the different spot lists
all_spot_lists = get_spot_lists()
url_spots_list = all_spot_lists[0]
spots_list = all_spot_lists[1]
country_code_list = all_spot_lists[2]

print(len(url_spots_list))
print(len(spots_list))
print(len(country_code_list))"""


def execute(num):
    try:
        all_spot_lists = get_spot_lists()
        url_spots_list = all_spot_lists[0]
        spots_list = all_spot_lists[1]
        country_code_list = all_spot_lists[2]

        print(len(url_spots_list))
        print(len(spots_list))
        print(len(country_code_list))

        print("-----------" + str(round(num/len(url_spots_list)*100)) + "% Progress-----------")
        current_spot_url = url_spots_list[num]

        # start with the normal forecast
        web_start = time.time()
        page = requests.get("https://www.windfinder.com/forecast/" + current_spot_url)
        soup = BeautifulSoup(page.content, "html.parser")

        print(current_spot_url)

        # get list with all wind speeds (gusts and speed)
        result_list = get_wind_and_gusts_list(soup)
        wind_speed_list = result_list[0]
        wind_gusts_list = result_list[1]

        # get the soup with all the dates
        result_list = get_day_lists(soup, 8)
        day_list = result_list[0]
        weekday_list = result_list[1]
        month_list = result_list[2]

        # get all the hours from the website remove the h and put them in the hour list
        hour_list = get_hours_list(soup)

        # get the wind directions
        wind_direction_list = get_wind_direction_list(soup)

        # get the wave height list
        wave_height_list = get_wave_height_list(soup)

        # get the wave period list
        wave_period_list = get_wave_period_list(soup)

        # get the wave direction list
        wave_direction_list = get_wave_direction_list(soup)

        # get the code for the weather without the rain (checks the name of the class)
        result_list = get_weather_and_day_list(soup)
        weather_list = result_list[0]
        is_day_list = result_list[1]

        # get the rain list with number None,1-5
        rain_list = get_rain_list(soup)

        # combine the three lists weather,day,rain to one with the swift icons
        weather_icon_list = decode_weather(weather_list, is_day_list, rain_list, len(weather_list))

        # get the temperature_list
        temperature_list = get_temperature_list(soup)

        # get the current_spot name (not in url)
        current_spot = spots_list[num]
        # get the country code
        country_code = country_code_list[num]

        # get the coordinates
        result_list = get_cooridnates(soup)
        latitude = float(result_list[0])
        longitude = float(result_list[1])

        #get the current wind and is_weather_station
        result_list = get_current_wind_and_is_weather_station(soup)
        current_wind = result_list[0]
        current_wind_direction = result_list[1]
        current_temperature = result_list[2]
        is_weather_station = result_list[3]

        ############################
        #do the superforecast webscraping
        page_super = requests.get("https://www.windfinder.com/weatherforecast/" + current_spot_url)
        super_soup = BeautifulSoup(page_super.content, "html.parser")

        #if there is also a superforecast scrape it and combine the normal lists with the super forecast lists later on
        if is_superforecast_available(super_soup):

            #get the day, weekday, and month
            day_lists_super = get_day_lists_super(super_soup, 24)
            day_list_super = day_lists_super[0]
            day_list_super = convert_super_lists_to_24_without_average(day_list_super)
            weekday_list_super = day_lists_super[1]
            weekday_list_super = convert_super_lists_to_24_without_average(weekday_list_super)
            month_list_super = day_lists_super[2]
            month_list_super = convert_super_lists_to_24_without_average(month_list_super)

            # get the hour list super
            hours_list_super = get_hours_list(super_soup)
            hours_list_super = convert_super_lists_to_24_without_average(hours_list_super)

            # get super wind direction in list
            wind_direction_list_super = get_wind_direction_list(super_soup)
            wind_direction_list_super = convert_super_lists_to_24_without_average(wind_direction_list_super)

            # get wind and gust lists in super
            wind_and_gusts_list_super = get_wind_and_gusts_list(super_soup)
            wind_speed_list_super = wind_and_gusts_list_super[0]
            wind_speed_list_super = convert_super_lists_to_24_average(wind_speed_list_super, 0)
            wind_gusts_list_super = wind_and_gusts_list_super[1]
            wind_gusts_list_super = convert_super_lists_to_24_average(wind_gusts_list_super, 0)

            # get the weather and is day list in super
            weather_and_day_list_super = get_weather_and_day_list(super_soup)
            weather_list_super = weather_and_day_list_super[0]
            weather_list_super = convert_super_lists_to_24_without_average(weather_list_super)
            is_day_list_super = weather_and_day_list_super[1]
            is_day_list_super = convert_super_lists_to_24_without_average(is_day_list_super)

            # get the rain list super
            rain_list_super = get_rain_list(super_soup)
            rain_list_super = convert_super_lists_to_24_without_average(rain_list_super)

            #generate the weather_icons:
            #check if we need 24 or 16 weather icons
            if len(rain_list_super) == 16:
                weather_icon_list_super = decode_weather(weather_list_super, is_day_list_super, rain_list_super, 16)
            elif len(rain_list_super) == 24:
                weather_icon_list_super = decode_weather(weather_list_super, is_day_list_super, rain_list_super, 24)
            else:
                weather_icon_list_super = []
                print("Couldn't find any correct weather icon length with super forecast")

            # get the temperature list super
            temperature_list_super = get_temperature_list_super(super_soup)
            temperature_list_super = convert_super_lists_to_24_average(temperature_list_super, 0)

            # get the wave direction list super
            wave_direction_list_super = get_wave_direction_list(super_soup)
            wave_direction_list_super = convert_super_lists_to_24_without_average(wave_direction_list_super)

            # get the wave height super list
            wave_height_list_super = get_wave_height_list(super_soup)
            wave_height_list_super = convert_super_lists_to_24_average(wave_height_list_super, 1)

            # get the wave period super list
            wave_period_list_super = get_wave_period_list(super_soup)
            wave_period_list_super = convert_super_lists_to_24_average(wave_period_list_super, 0)

            #####################################################################################################

            #combine the super forecast and normal forecast lists
            wind_speed_list = combine_normal_and_superforecast(wind_speed_list, wind_speed_list_super)
            wind_gusts_list = combine_normal_and_superforecast(wind_gusts_list, wind_gusts_list_super)
            day_list = combine_normal_and_superforecast(day_list, day_list_super)
            weekday_list = combine_normal_and_superforecast(weekday_list, weekday_list_super)
            month_list = combine_normal_and_superforecast(month_list, month_list_super)
            hour_list = combine_normal_and_superforecast(hour_list, hours_list_super)
            wind_direction_list = combine_normal_and_superforecast(wind_direction_list, wind_direction_list_super)
            wave_height_list = combine_normal_and_superforecast(wave_height_list, wave_height_list_super)
            wave_period_list = combine_normal_and_superforecast(wave_period_list, wave_period_list_super)
            wave_direction_list = combine_normal_and_superforecast(wave_direction_list, wave_direction_list_super)
            weather_icon_list = combine_normal_and_superforecast(weather_icon_list, weather_icon_list_super)
            temperature_list = combine_normal_and_superforecast(temperature_list, temperature_list_super)


        #send all the lists to the write_to_json.py to make it a json_file format
        json_file = write_to_json(country_code, is_weather_station, current_spot, latitude, longitude,
                                  month_list, day_list, weekday_list, hour_list, current_wind, current_wind_direction,
                                  wind_speed_list, wind_gusts_list, wind_direction_list,
                                  wave_height_list, wave_period_list, wave_direction_list,
                                  weather_icon_list, current_temperature, temperature_list)


        save_start = time.time()
        #sort the json file alphabetically
        #json_file = sorted(json_file, key=lambda k: (k['country_code'], k["spot"]))

        #export and save the json file
        file_name = current_spot_url + ".json"
        with open(file_name, "w") as f:
            json.dump(json_file, f, indent=2)
        savesh(current_spot_url)

        save_end = time.time()
    except:
        print("error")


