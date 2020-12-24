month_name_to_int_dict = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def convert_month_name_to_int(month_name):
    return month_name_to_int_dict[month_name]


def decode_weather(weather_list, is_day_list, rain_list, n):
    weather_icon = []

    for index in range(n):
        working_weather = weather_list[index]
        working_rain = rain_list[index]
        working_is_day = is_day_list[index]

        # check which kind of weather/rain/day combination it is and append the correct swift name for the icon
        # terminology: working_weather:clear/medium/full;
        #             working_rain:1,2,3(for rain), 4(for snow);
        #             working_is_day:True(day), False(night)
        if working_rain == 4:
            if working_weather == "clear":
                weather_icon.append("snow")
            else:
                weather_icon.append("cloud.snow.fill")
        elif working_rain == 5:
            weather_icon.append("cloud.sleet.fill")
        elif working_weather == "clear" and working_rain is None:
            if working_is_day:
                weather_icon.append("sun.max.fill")
            else:
                weather_icon.append("moon.fill")
        elif working_weather == "medium" and working_rain is None:
            if working_is_day:
                weather_icon.append("cloud.sun.fill")
            else:
                weather_icon.append("cloud.moon.fill")
        elif working_weather == "cloudy":
            if working_rain is None:
                weather_icon.append("cloud.fill")
            elif working_rain == 1:
                weather_icon.append("cloud.drizzle.fill")
            elif working_rain == 2:
                weather_icon.append("cloud.rain.fill")
            else:
                weather_icon.append("cloud.heavyrain.fill")
        else:
            if working_is_day:
                weather_icon.append("cloud.sun.rain.fill")
            else:
                weather_icon.append("cloud.moon.rain.fill")

    return weather_icon

def convert_super_lists_to_24_average(old_list, num_of_deci_round):
    index_list_three_days = [6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 34, 36, 38, 40, 42, 44, 54, 56, 58, 60, 62, 64, 66,
                             68]
    index_list_two_days = [6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 34, 36, 38, 40, 42, 44]
    new_list = []
    if len(old_list) >= 70:
        for each in index_list_three_days:
            new_value = round((old_list[each] + old_list[each + 1]) / 2, num_of_deci_round)
            new_list.append(new_value)
        return new_list
    else:
        for each in index_list_two_days:
            new_value = round((old_list[each] + old_list[each + 1]) / 2)
            new_list.append(new_value)
        return new_list


#convert lists from the superforecast to 24/16 values for the hours 6,8,10... with the first and no average
def convert_super_lists_to_24_without_average(old_list):
    index_list_three_days = [6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 34, 36, 38, 40, 42, 44, 54, 56, 58, 60, 62, 64, 66, 68]
    index_list_two_days = [6, 8, 10, 12, 14, 16, 18, 20, 30, 32, 34, 36, 38, 40, 42, 44]
    new_list = []
    #needs 70 to do three days (especially for the lists with average)
    if len(old_list) >= 70:
        for each in index_list_three_days:
            new_value = old_list[each]
            new_list.append(new_value)
        return new_list
    else:
        for each in index_list_two_days:
            new_value = old_list[each]
            new_list.append(new_value)
        return new_list




def combine_normal_and_superforecast(normal_list, super_list):
    length = len(super_list)
    normal_list = normal_list[length:]
    result_list = super_list + normal_list
    return result_list


def is_superforecast_available(super_soup):
    super_soup = super_soup.find("title").text
    if "Document not found" in super_soup:
        return False
    else:
        return True
