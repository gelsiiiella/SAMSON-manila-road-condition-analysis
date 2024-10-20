#Template code
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from data_fetch import fetch_manila_roads, fetch_mapillary_images
from model_utils import load_cnn_model, predict_road_conditions
from visualization import create_folium_map, folium_to_html

# Create Dash app
app = Dash(__name__)

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Manila Road Conditions Visualization"),
    html.Button("Fetch Data and Update Map", id='fetch-data', n_clicks=0),
    html.Div(id='map')
])

# Callback to update the map
@app.callback(
    Output('map', 'children'),
    Input('fetch-data', 'n_clicks')
)
def update_map(n_clicks):
    if n_clicks is None:
        return html.Div()

    # Fetch road data
    roads_gdf = fetch_manila_roads()
    
    # Fetch images from Mapillary
    fetch_mapillary_images(roads_gdf)

    # Load the trained CNN model
    model = load_cnn_model()

    # Predict road conditions
    conditions = predict_road_conditions(model)

    # Create a Folium map with road conditions
    folium_map = create_folium_map(roads_gdf, conditions)

    # Convert Folium map to HTML
    folium_map_html = folium_to_html(folium_map)

    return dcc.Markdown(folium_map_html, dangerously_allow_html=True)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
