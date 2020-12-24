def get_wind_and_gusts_list(soup):
    wind_speed_and_gusts_soup = soup.find_all("span", class_="units-ws")
    # set a counter to check if its odd or even to check if gust or normal wind speed
    counter = 0
    # define the lists to store the data
    wind_speed_list = []
    wind_gusts_list = []
    # go through each item and add it to the corresponding list (speed or gusts)
    for each in wind_speed_and_gusts_soup:
        if counter % 2 == 0:
            wind_speed_list.append(int(each.text))
        else:
            wind_gusts_list.append(int(each.text))
        counter += 1
    return [wind_speed_list, wind_gusts_list]


def get_day_lists(soup, repeat_num):
    from operators import convert_month_name_to_int
    dates_soup = soup.find_all("h3", class_="h h--4 weathertable__headline")
    # define the month and day lists
    month_list = []
    day_list = []
    weekday_list = []
    # seperate them get the raw text and edit it to only the day and month
    for each in dates_soup:
        unedited_date = each.text
        # remove all the spaces and \n at the beginning
        while unedited_date[0] == " " or unedited_date[0] == "\n":
            unedited_date = unedited_date[1:]
        # get the day of the week (monday..)
        weekday = unedited_date[:unedited_date.index(",")]
        # get the month in string
        unedited_date = unedited_date[unedited_date.index(",") + 2:]
        month_name = unedited_date[:3]
        # get the day in string
        unedited_date = unedited_date[4:]
        day = unedited_date[:unedited_date.index("\n")]
        month = convert_month_name_to_int(month_name)
        # put the day and month 8 times in the lists
        for i in range(repeat_num):
            month_list.append(int(month))
            day_list.append(int(day))
            weekday_list.append(weekday)
    return [day_list, weekday_list, month_list]


def get_day_lists_super(soup, repeat_num):
    from operators import convert_month_name_to_int
    dates_soup = soup.find_all("h3", class_="weathertable__headline")
    # define the month and day lists
    month_list = []
    day_list = []
    weekday_list = []
    # seperate them get the raw text and edit it to only the day and month
    for each in dates_soup:
        unedited_date = each.text
        # remove all the spaces and \n at the beginning
        while unedited_date[0] == " " or unedited_date[0] == "\n":
            unedited_date = unedited_date[1:]
        # get the day of the week (monday..)
        weekday = unedited_date[:unedited_date.index(",")]
        # get the month in string
        unedited_date = unedited_date[unedited_date.index(",") + 2:]
        month_name = unedited_date[:3]
        # get the day in string
        unedited_date = unedited_date[4:]
        day = unedited_date[:unedited_date.index("\n")]
        month = convert_month_name_to_int(month_name)
        # put the day and month 8 times in the lists
        for i in range(repeat_num):
            month_list.append(int(month))
            day_list.append(int(day))
            weekday_list.append(weekday)
    return [day_list, weekday_list, month_list]


def get_hours_list(soup):
    hour_soup = soup.find_all("div", class_="cell-timespan weathertable__cellgroup weathertable__cellgroup--stacked")
    hour_list = []
    for each in hour_soup:
        each = each.find("span")
        unedited_hour = each.text
        hour = unedited_hour[:unedited_hour.index("h")]
        hour_list.append(int(hour))
    return hour_list


def get_wind_direction_list(soup):
    direction_soup = soup.find_all("div", class_="cell-wind-2 weathertable__cellgroup weathertable__cellgroup--stacked")
    wind_direction_list = []
    for each in direction_soup:
        each = each.text
        # define unedited direction and go through each letter of the each.text to only add the numbers and letters
        unedited_direction = ""
        for each_letter in each:
            if each_letter != " " and each_letter != "\n":
                unedited_direction += each_letter
        wind_direction = unedited_direction[:unedited_direction.index("°")]
        wind_direction_list.append(int(wind_direction))
    return wind_direction_list


def get_wave_height_list(soup):
    wave_height_block_soup = soup.find_all("div", class_="data-waveheight data--major weathertable__cell")
    wave_height_list = []
    for each in wave_height_block_soup:
        wave_height_list.append(float(each.find("span", "units-wh").text))

    #append 0 that in total its 80 values
    for num123 in range(80-len(wave_height_list)):
        wave_height_list.append(0)

    return wave_height_list


def get_wave_period_list(soup):
    wave_period_soup = soup.find_all("div", class_="data-wavefreq data--minor weathertable__cell")
    wave_period_list = []
    for each in wave_period_soup:
        each = each.text
        while each[0] == "\n" or each[0] == " ":
            each = each[1:]
        each = each[:-3]
        wave_period_list.append(int(each))

    # append 0 that in total its 80 values
    for num123 in range(80 - len(wave_period_list)):
        wave_period_list.append(0)

    return wave_period_list


def get_wave_direction_list(soup):
    wave_direction_list = []
    wave_direction_soup = soup.find_all("div", class_="data-direction-arrow weathertable__cell units-wad-sym")
    for each in wave_direction_soup:
        each2 = each.find("div")
        each = each2.get("title")
        each = float(each[:-1])
        each = round(each)
        each = int(each)
        wave_direction_list.append(each)

    # append 0 that in total its 80 values
    for num123 in range(80 - len(wave_direction_list)):
        wave_direction_list.append(0)

    return wave_direction_list


def get_weather_and_day_list(soup):
    weather_symbol_code_list = []
    weather_symbol_soup = soup.find_all("div", class_="data-cover weathertable__cell")
    for each in weather_symbol_soup:
        classes = [value
                   for element in each.find_all(class_=True)
                   for value in element["class"]]
        weather_symbol_code = classes[1]
        weather_symbol_code_list.append(weather_symbol_code)
    # change the weather symbol code to clear, medium, cloudy
    weather_list = []
    is_day_list = []
    # first for day and night then for the type of weather
    for each in weather_symbol_code_list:
        each = each[each.index("-") + 1:]
        if each[0] == "d":
            is_day_list.append(True)
        else:
            is_day_list.append(False)
        each = each[2:]
        if each == "skc":
            weather_list.append("clear")
        elif each == "few" or each == "sct" or each == "bkn":
            weather_list.append("medium")
        else:
            weather_list.append("cloudy")
    return [weather_list, is_day_list]


def get_rain_list(soup):
    rain_code_list = []
    rain_soup = soup.find_all("div", class_="data-preciptype weathertable__cell")
    for each in rain_soup:
        classes = [value
                   for element in each.find_all(class_=True)
                   for value in element["class"]]
        if len(classes) == 0:
            rain_code_list.append(None)
        else:
            rain_code_list.append(classes[0])
    # change the rain code to int (1,2,3 for rain and 4 for any kind of snow and 5 for any snowrain)
    rain_list = []
    for each in rain_code_list:
        if each is None:
            rain_list.append(None)
        elif each == 'icon-rain-1':
            rain_list.append(1)
        elif each == 'icon-rain-2':
            rain_list.append(2)
        elif each == 'icon-rain-3':
            rain_list.append(3)
        elif each[:-1] == "icon-snow-":
            rain_list.append(4)
        elif each[:-1] == "icon-rainsnow-":
            rain_list.append(5)
        else:
            print("Error with the rain amount")
    return rain_list


def get_temperature_list(soup):
    temperature_list = []
    temperature_soup = soup.find_all("span", class_="units-at")
    for each in temperature_soup:
        temperature_list.append(int(each.text))
    return temperature_list


def get_temperature_list_super(soup):
    temperature_list = []
    temperature_soup = soup.find_all("span", class_="units-at")
    #define a counter to just add every second item to list
    counter = 0
    for each in temperature_soup:
        if counter % 2 == 0:
            temperature_list.append(int(each.text))
        counter += 1
    return temperature_list


def get_cooridnates(soup):
    coordinate_soup = soup.find("a", class_="siteheader-mapsbutton icon-back-to-maps")
    href = coordinate_soup.get("href")
    href = href[href.index("/") + 1:]
    href = href[href.index("/") + 1:]
    latitude = href[:href.index("/")]
    longitude = href[href.index("/") + 1:]

    return [latitude, longitude]

#get the current wind, wind direction, temperature and wether it is a real weather station
def get_current_wind_and_is_weather_station(soup):
    # get the script tags
    soup = soup.findAll("script")

    # get the current wind speed by searching the script at index 18 for the expression "ws: " and take the number behind it
    possible_string = soup[18].prettify()
    wind_index = possible_string.index("ws:")
    possible_wind_string = possible_string[wind_index + 4: wind_index + 10]
    possible_wind_string = possible_wind_string[:possible_wind_string.index(",")]
    #try because sometimes there is no value at all (maybe weather_station turned off)
    try:
        current_wind_speed = int(round(float(possible_wind_string)))
    except:
        current_wind_speed = 0

    #get the current wind_direction (similar to the current_wind)
    wind_direction_index = possible_string.index("wd:")
    possible_wind_direction_string = possible_string[wind_direction_index + 4: wind_direction_index + 11]
    possible_wind_direction_string = possible_wind_direction_string[:possible_wind_direction_string.index(",")]
    # try because sometimes there is no value at all (maybe weather_station turned off)
    try:
        current_wind_direction = int(round(float(possible_wind_direction_string)))
    except:
        current_wind_direction = 0

    #get the current temperature
    current_temperature_index = possible_string.index(" at: ")
    current_temperature_string = possible_string[current_temperature_index + 5: current_temperature_index + 12]
    current_temperature_string = current_temperature_string[:current_temperature_string.index(",")]
    # try because sometimes there is no value at all (maybe weather_station turned off)
    try:
        current_temperature = int(round(float(current_temperature_string)))
    except:
        current_temperature = 0

    # take the possible string from before (script at index 18) and check if it can find isReport: true
    is_weather_station = True
    try:
        is_weather_station_index = possible_string.index("isReport: true")
    except:
        is_weather_station = False

    return [current_wind_speed, current_wind_direction, current_temperature, is_weather_station]

