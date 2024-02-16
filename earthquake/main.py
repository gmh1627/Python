import plotly.express as px
import json
import pandas as pd
filename='data/eq_data_30_day_m1.json'
with open(filename) as f:
    all_eq_data=json.load(f)
readable_file='data/readable_eq_data.json'
with open(readable_file,'w')as f:
    json.dump(all_eq_data,f,indent=4)
all_eq_dicts=all_eq_data['features']
print("地震次数:\n",len(all_eq_dicts))
mags,titles,lons,lats=[],[],[],[]
for eq_dict in all_eq_dicts:
    mag=eq_dict['properties']['mag']
    title=eq_dict['properties']['title']
    lon=eq_dict['geometry']['coordinates'][0]
    lat=eq_dict['geometry']['coordinates'][1]
    mags.append(mag)
    titles.append(title)
    lons.append(lon)
    lats.append(lat)
data=pd.DataFrame(
    data=zip(lons,lats,titles,mags),columns=['longitude','latitude','location','magnitude']
)
data.head()
fig=px.scatter(
    data,
    x='longitude',
    y='latitude',
    labels={'x':'longitude','y':'latitude'},
    range_x=[-180,180],
    range_y=[-90,90],
    width=800,
    height=800,
    size='magnitude',
    size_max=10,
    color='magnitude',
    hover_name='location',
)
fig.write_html('gobal_earthquakes.html')
fig.show()