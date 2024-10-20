import os
import requests
import osmnx as ox
import geopandas as gpd

# Mapillary API Key here
MAPILLARY_API_KEY = 'YOUR_MAPILLARY_API_KEY'

# Fetch the road network for Manila
def fetch_manila_roads():
    location = "Manila, Philippines"
    graph = ox.graph_from_place(location, network_type='drive')
    roads_gdf = ox.graph_to_gdfs(graph, nodes=False, edges=True)
    return roads_gdf

# Fetch images from Mapillary
def fetch_mapillary_images(roads_gdf, image_dir='road_images'):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    for i, row in roads_gdf.iterrows():
        # Get the coordinates of the road geometry
        coords = row['geometry'].coords
        lat, lon = coords[0][1], coords[0][0]

        # Mapillary API to fetch images near the road
        url = f"https://api.mapillary.com/v3/images?closeto={lon},{lat}&access_token={MAPILLARY_API_KEY}&limit=5"
        response = requests.get(url)
        
        if response.status_code == 200:
            images = response.json()
            for j, img in enumerate(images):
                image_url = img['key']  # This is the Mapillary image key
                # Construct the image URL
                img_url = f"https://images.mapillary.com/{image_url}/640.jpg"
                img_data = requests.get(img_url).content
                with open(os.path.join(image_dir, f'road_{i}_{j}.jpg'), 'wb') as handler:
                    handler.write(img_data)
        else:
            print(f"Failed to fetch images for road {row['name']}: {response.status_code}")
