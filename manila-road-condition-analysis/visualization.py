import folium

# Create Folium Map with conditions
def create_folium_map(roads_gdf, conditions):
    m = folium.Map(location=[14.5995, 120.9842], zoom_start=12)

    # Add road lines to the map
    for idx, row in roads_gdf.iterrows():
        color = 'green' if conditions[idx] == 0 else 'orange' if conditions[idx] == 1 else 'red'
        
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color: {
                'color': color,
                'weight': 2,
                'opacity': 0.7,
            },
            tooltip=row['name']
        ).add_to(m)

    return m

# Function to convert folium map to HTML
def folium_to_html(m):
    return m._repr_html_()
