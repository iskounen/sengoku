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
  '讃岐': '細川',
  '土佐': '細川',
  '和泉': '細川',
  '備中': '細川',
  '淡路': '細川*',
  '阿波': '細川*',
  '河内': '畠山',
  '紀伊': '畠山',
  '越中': '畠山',
  '能登': '畠山*',
  '播磨': '山名',
  '但馬': '山名',
  '備後': '山名',
  '備前': '山名',
  '美作': '山名',
  '石見': '山名',
  '山城': '山名',
  '因幡': '山名',
  '伯耆': '山名',
  '安芸': '山名',
  '若狭': '武田',
  '丹後': '一色',
  '三河': '細川',
  '出雲': '京極',
  '隠岐': '京極',
  '飛騨': '京極',
  '美濃': '土岐',
  '伊勢': '北畠',
  '志摩': '北畠',
  '駿河': '今川',
  '周防': '大内',
  '長門': '大内',
  '筑前': '大内',
  '筑後': '菊池',
  '豊前': '大内',
  '豊後': '大友',
  '肥前': '渋川',
  '肥後': '菊池',
  '日向': '島津',
  '薩摩': '島津',
  '大隅': '島津',
  '武蔵': '上杉',
  '上野': '上杉',
  '越後': '上杉*',
  '下野': '小山',
  '近江': '六角',
  '信濃': '小笠原',
  '加賀': '富樫',
  '対馬': '宗',
}

# Map clans to colors
clan_to_color = {
  '斯波': 'red',
  '細川': 'blue',
  '細川*': 'cyan',
  '畠山': 'green',
  '畠山*': 'lime',
  '山名': 'purple',
  '武田': 'orange',
  '一色': 'yellow',
  '京極': 'magenta',
  '今川': 'maroon',
  '大内': 'black',
  '大友': 'brown',
  '菊池': 'pink',
  '渋川': 'olive',
  '島津': 'navy',
  '北畠': 'gray',
  '上杉': 'mediumspringgreen',
  '上杉*': 'mediumseagreen',
  '六角': 'hotpink',
  '土岐': 'darkorange',
  '小笠原': 'darkblue',
  '小山': 'darkred',
  '富樫': 'tomato',
  '宗': 'dodgerblue',
}

def style_function(feature):
    province_name = feature['properties']['国名']
    clan_name = province_to_clan.get(province_name, '未設定')
    return {
        'fillColor': clan_to_color.get(clan_name, 'none'),
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.4,
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
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=7, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')

# Add the GeoJSON data to the map
folium.GeoJson(
    geo_data,
    style_function=style_function,
    highlight_function=highlight_function,
).add_to(m)

# Define a legend
legend_html = '''
<div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 500px; border: 2px solid grey; z-index: 9999; font-size: 14px; background-color: white;">
&nbsp;<i style="background: red; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;斯波<br>
&nbsp;<i style="background: blue; width: 12px; height: 10px; display: inline-block;"></i><i style="background: cyan; width: 12px; height: 10px; display: inline-block;"></i>&nbsp;細川<br>
&nbsp;<i style="background: green; width: 12px; height: 10px; display: inline-block;"></i><i style="background: lime; width: 12px; height: 10px; display: inline-block;"></i>&nbsp;畠山<br>
<br>
&nbsp;<i style="background: purple; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;山名<br>
&nbsp;<i style="background: yellow; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;一色<br>
&nbsp;<i style="background: magenta; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;京極<br>
<br>
&nbsp;<i style="background: mediumspringgreen; width: 12px; height: 10px; display: inline-block;"></i><i style="background: mediumseagreen; width: 12px; height: 10px; display: inline-block;"></i>&nbsp;上杉<br>
&nbsp;<i style="background: darkblue; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;小笠原<br>
&nbsp;<i style="background: darkred; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;小山<br>
&nbsp;<i style="background: tomato; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;富樫<br>
&nbsp;<i style="background: orange; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;武田<br>
&nbsp;<i style="background: maroon; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;今川<br>
&nbsp;<i style="background: gray; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;北畠<br>
&nbsp;<i style="background: hotpink; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;六角<br>
&nbsp;<i style="background: darkorange; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;土岐<br>
&nbsp;<i style="background: darkblue; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;小笠原<br>
&nbsp;<i style="background: black; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;大内<br>
&nbsp;<i style="background: brown; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;大友<br>
&nbsp;<i style="background: pink; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;菊池<br>
&nbsp;<i style="background: olive; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;渋川<br>
&nbsp;<i style="background: navy; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;島津<br>
&nbsp;<i style="background: dodgerblue; width: 24px; height: 10px; display: inline-block;"></i>&nbsp;宗<br>
</div>
'''

# Add the legend to the map
m.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
m.save('map.html')

print("Map has been saved to map.html")