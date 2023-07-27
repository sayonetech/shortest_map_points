import os
import json

from dotenv import load_dotenv

from find_shortest_points import get_sferiche_pois, get_sferiche_selected_points, get_data_from_url

load_dotenv()


# Long - X(small), Lat - Y(Big)

MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
FETCH_FROM_FILE = True if os.getenv('FETCH_FROM_FILE') == 'True' else False
DISTANCE_THRESHOLD = 5  # exclude point if the distance in grater than 5

SFERICHE_URL = "https://dev.phygital.bbsitalia.com/sites/default/files/sferiche/sferiche.json"
POI_URL = "https://dev.phygital.bbsitalia.com/poi-simplified.json"


# Load all sferiche points
if FETCH_FROM_FILE:
    with open('data/sferiche.json', 'r') as f:
      sferiche_data = json.load(f)
else:
    sferiche_data = get_data_from_url(SFERICHE_URL)

all_sferiche = []
for sferiche in sferiche_data['sferiche']:
    all_sferiche.append([float(sferiche['X']),float(sferiche['Y'])])


# Load input data
if FETCH_FROM_FILE:
    input_data = {
        "Pois": [
            {
                "Id_poi": 1,
                "Lat" : "44.404096",
                "Long": "8.93136"
            },
            {
                "Id_poi": 2,
                "Lat" : "44.403877",
                "Long": "8.933102"
            }
        ]
    }
else:
    input_data = get_data_from_url(POI_URL)

sferiche_pois = get_sferiche_pois(input_data, all_sferiche)

# For now it assumes 2 points as input
sferiche_selected_points = get_sferiche_selected_points(
    sferiche_pois,  all_sferiche, mapbox_token=MAPBOX_ACCESS_TOKEN,
    distance_threshhold=DISTANCE_THRESHOLD
)
all_result = sferiche_pois[:1] + sferiche_selected_points + sferiche_pois[1:]

all_result_dict = {
    "spheriche": all_result
}

print(json.dumps(all_result_dict))
