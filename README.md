# shortest_map_points

#### How to run
 - python3 -m venv ../virtual
 - source ../virtual/bin/activate
 - pip install -r requirements.txt
 - Create .env file paste content inside .env.example with correct values(It requires MapBox access token - https://docs.mapbox.com/playground/directions/)
 - set FETCH_FROM_FILE True(from file) or False(From URL)\
 - python find_shortest_points.py
   (This will print the track json)