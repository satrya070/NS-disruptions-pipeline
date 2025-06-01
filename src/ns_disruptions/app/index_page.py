import streamlit as st
import folium
import altair as alt
import pandas as pd
import logging
import shapely

from streamlit_folium import st_folium

logging.basicConfig(level=logging.INFO)


st.title("NS disruption data")

@st.cache_data()
def fetch_data():
    logging.info("fetch_data was called")
    conn = st.connection("postgresql", type="sql")

    df_map_data = conn.query("SELECT * FROM ns.map_data")
    df_day_stats = conn.query("SELECT * FROM ns.day_aggregations")
    df_affected_stations = conn.query(
        "SELECT name, involved_disruptions, station_type, effects FROM ns.affected_stations_24h")

    conn.session.close()
    return df_map_data, df_day_stats, df_affected_stations

# fetch the data first
df_map_data, df_day_stats, df_affected_stations = fetch_data()

# init map
m = folium.Map(location=[52.552474, 5.188491], zoom_start=8, tiles="Cartodb Positron")

# add all map points
for row in df_map_data.itertuples():
    location = shapely.from_wkb(row.location)
    #print(location.x)
    logging.info(row.location)
    folium.Circle(
        location=[location.x, location.y],
        radius=200,
        color="red",
        weight=2,
        fill=True,
        fill_color="red",
        fill_opacity=0.6,
        tooltip=row.name,
    ).add_to(m)

# render map
st.subheader("Affected stations in the last 24 hours")
with st.container(height=800):
    st_data = st_folium(m, use_container_width=True, height=700)

# display affected stations -----------------------------------
st.subheader("List of affected stations in the last 24 hours")
st.dataframe(df_affected_stations, use_container_width=True)

# render stats last 30d on day level ---------------------------------------
st.subheader("Number of disruptions per day")
# format the timestamp col to datetime
df_day_stats["day"] = pd.to_datetime(df_day_stats["day"])
df_day_stats["day"] = df_day_stats["day"].dt.strftime("%Y-%m-%d")

bars = alt.Chart(df_day_stats).mark_bar().encode(
        y=alt.Y("day:N", title="Date"),
        x=alt.X("count:Q", stack="zero", title="Number of disruptions"),
        color=alt.Color("type:N", title="Type")
)

# text layer
text = alt.Chart(df_day_stats).mark_text(dx=-12, dy=0, color="black", baseline="middle").encode(
    y=alt.Y("day:N"),
    x=alt.X("count:Q", stack="zero"),
    detail="type:N",
    text=alt.Text("count:Q")
)

final_chart = bars + text

st.altair_chart(final_chart, use_container_width=True)



