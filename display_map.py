import folium
import geopandas as gpd

# Read the GeoJSON file
geojson_file = 'map.geojson'
geo_data = gpd.read_file(geojson_file)

# Map provinces to clans
province_to_clan = {
  '越前': '斯波',
  '尾張': '斯波',
  '遠江': '斯波',
  '丹波': '細川',
  '摂津': '細川',
  '阿波': '細川*',
  '讃岐': '細川',
  '土佐': '細川',
  '淡路': '細川*',
  '河内': '畠山',
  '紀伊': '畠山',
  '越中': '畠山',
  '能登': '畠山*',
  '播磨': '山名',
  '但馬': '山名',
  '備後': '山名',
  '備前': '山名',
  '美作': '山名',

}

# Map clans to colors
clan_to_color = {
  '斯波': 'red',
  '細川': 'blue',
  '細川*': 'cyan',
  '畠山': 'green',
  '畠山*': 'lime',
  '山名': 'purple',
}

def style_function(feature):
    province_name = feature['properties']['国名']
    clan_name = province_to_clan.get(province_name, '未設定')
    return {
        'fillColor': clan_to_color.get(clan_name, 'none'),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5,
    }

def highlight_function(feature):
    province_name = feature['properties']['国名']
    clan_name = province_to_clan.get(province_name, '未設定')
    return {
        'fillColor': clan_to_color.get(clan_name, 'none'),
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.7,
    }

# Calculate the centroids in the projected CRS
centroid = geo_data.geometry.union_all().centroid

# Create a folium map centered around the GeoJSON data
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=8)

# Add the GeoJSON data to the map
folium.GeoJson(
    geo_data,
    style_function=style_function,
    highlight_function=highlight_function,
).add_to(m)

# Define a legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 200px; border: 2px solid grey; z-index: 9999; font-size: 14px; background-color: white;">
&nbsp;<b>Legend</b><br>
&nbsp;<i style="background: red; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;斯波<br>
&nbsp;<i style="background: blue; width: 12px; height: 10px; display: inline-block;"></i><i style="background: cyan; width: 12px; height: 10px; display: inline-block;"></i>&nbsp;細川<br>
&nbsp;<i style="background: green; width: 12px; height: 10px; display: inline-block;"></i><i style="background: lime; width: 12px; height: 10px; display: inline-block;"></i>&nbsp;畠山<br>
<br>
&nbsp;<i style="background: purple; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;山名<br>
</div>
'''

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
m.save('map.html')

print("Map has been saved to map.html")