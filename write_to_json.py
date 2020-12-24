def write_to_json(country_code, is_weather_station, spot, latitude, longitude,
                  month_list, day_list, weekday_list, hour_list,
                  current_wind, current_wind_direction, wind_speed_list,
                  wind_gusts_list, wind_direction_list, wave_height_list, wave_period_list, wave_direction_list,
                  weather_icon_list, current_temperature, temperature_list):
    final_dict = {
        "spot": spot,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude
        },
        "country_code": country_code,
        "is_weather_station": is_weather_station,
        "month": month_list,
        "day": day_list,
        "weekday": weekday_list,
        "hour": hour_list,
        "current_wind": current_wind,
        "current_wind_direction": current_wind_direction,
        "wind_speed": wind_speed_list,
        "wind_gusts": wind_gusts_list,
        "wind_direction": wind_direction_list,
        "wave_height": wave_height_list,
        "wave_period": wave_period_list,
        "wave_direction": wave_direction_list,
        "weather_icon": weather_icon_list,
        "current_temperature": current_temperature,
        "temperature": temperature_list
    }
    json_file = final_dict

    return json_file
