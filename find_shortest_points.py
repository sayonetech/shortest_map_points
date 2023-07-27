import os
import json
import requests

from scipy.spatial import distance
from dotenv import load_dotenv

load_dotenv()


# Long - X(small), Lat - Y(Big)

MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN')
FETCH_FROM_FILE = True if os.getenv('FETCH_FROM_FILE') == 'True' else False

SFERICHE_URL = "https://dev.phygital.bbsitalia.com/sites/default/files/sferiche/sferiche.json"
POI_URL = "https://dev.phygital.bbsitalia.com/poi-simplified.json"


def get_data_from_url(url):
    print('Loading from URL......: %s' % url)
    r = requests.get(url)
    if r.status_code != 200:
        print('Error from API, URL: %s, Response: %s' % (url, r.text))
        raise

    data = r.json()
    return data


# Load all sferiche points
if FETCH_FROM_FILE:
    with open('data/sferiche.json', 'r') as f:
      sferiche_data = json.load(f)
else:
    sferiche_data = get_data_from_url(SFERICHE_URL)

all_sferiche = []
for sferiche in sferiche_data['sferiche']:
    all_sferiche.append([float(sferiche['X']),float(sferiche['Y'])])


def closest_node_and_distance(node, nodes):
    # Format node = (long, lat)
    distances = distance.cdist([node], nodes)
    closest_index = distances.argmin()
    return nodes[closest_index], distances[0][closest_index]


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


def get_sferiche_pois():
    sferiche_pois = []
    for point_data in input_data['Pois']:
        lat, long = float(point_data['Lat']), float(point_data['Long'])
        point, dist = closest_node_and_distance((long, lat), all_sferiche)
        sferiche_pois.append({
            "id-poi": point_data['Id_poi'],
            "X": point[0],
            "Y": point[1],
        })
    return sferiche_pois


def prepare_sferiche_pois_for_route(sferiche_pois):
    points_str_list = []
    if len(sferiche_pois) < 2:
        raise Exception('Minimum 2 points needed')
    for sferiche_poi in sferiche_pois:
        points_str_list.append("%s,%s" % (sferiche_poi['X'], sferiche_poi['Y'],))

    return ';'.join(points_str_list)


def get_sferiche_selected_points():
    route_api = "https://api.mapbox.com/directions/v5/mapbox/walking/"\
            "%s?"\
            "alternatives=true&geometries=geojson&language=en&overview=full&steps=true&"\
            "access_token=%s" % (prepare_sferiche_pois_for_route(sferiche_pois), MAPBOX_ACCESS_TOKEN)

    data = get_data_from_url(route_api)

    routes = data['routes'][0]
    sferiche_selected = []
    _coordinates = []
    for coordinate in routes['geometry']['coordinates']:
        long, lat = coordinate[0], coordinate[1]
        point, dist = closest_node_and_distance((long, lat), all_sferiche)
        sferiche_selected.append({
            "id-poi": None,
            "X": point[0],
            "Y": point[1],
        })
        _coordinates.append([long, lat])
    return sferiche_selected


sferiche_pois = get_sferiche_pois()

# For now it assumes 2 points as input
all_result = sferiche_pois[:1] + get_sferiche_selected_points() + sferiche_pois[1:]

all_result_dict = {
    "spheriche": all_result
}

print(json.dumps(all_result_dict))
