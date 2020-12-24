from spot_lists import get_spot_lists
from scraping_tools import get_cooridnates
import requests
from bs4 import BeautifulSoup
import json
import time
from savesh import savesh

all_spot_lists = get_spot_lists()
url_spots_list = all_spot_lists[0]
spots_list = all_spot_lists[1]
country_code_list = all_spot_lists[2]

print(len(url_spots_list))
print(len(spots_list))
print(len(country_code_list))
main_json_file = []


for num in range(len(url_spots_list)):
    time.sleep(1)
    print("-----------" + str(round(num/len(url_spots_list)*100)) + "% Progress-----------")
    current_spot_url = url_spots_list[num]
    current_spot_name = spots_list[num]
    current_country_code = country_code_list[num]

    print(current_spot_url)

    # start with the normal forecast
    page = requests.get("https://www.windfinder.com/forecast/" + current_spot_url)
    soup = BeautifulSoup(page.content, "html.parser")

    result_list = get_cooridnates(soup)
    latitude = float(result_list[0])
    longitude = float(result_list[1])

    main_json_file.append({
        "spot": current_spot_name,
        "url_code": current_spot_url,
        "country_code": current_country_code,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude
        }
    })


#sort the json file alphabetically
main_json_file = sorted(main_json_file, key=lambda k: (k['country_code'], k["spot"]))

with open("main.json", "w") as f:
    json.dump(main_json_file, f, indent=2)
print(savesh("main"))
