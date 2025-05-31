import streamlit as st
import folium
import altair as alt
import pandas as pd

from streamlit_folium import st_folium


st.title("NS disruption data")

# init map
m = folium.Map(location=[52.552474, 5.188491], zoom_start=8, tiles="Cartodb Positron")

# add all data points
folium.Circle(
    location=[52.328762, 5.057319],
    radius=200,
    color="red",
    weight=2,
    fill=True,
    fill_color="red",
    fill_opacity=0.6,
    tooltip="test",
).add_to(m)

# render map
st_data = st_folium(m, width=725)

df = pd.DataFrame({
    'day': ['2025-05-28', '2025-05-28', '2025-05-29', '2025-05-29', '2025-05-30', '2025-05-30'],
    'type': ['DISRUPTION', 'MAINTENANCE', 'DISRUPTION', 'MAINTENANCE', 'DISRUPTION', 'MAINTENANCE'],
    'count': [4, 5, 3, 11, 2, 12]
})
df['day'] = pd.to_datetime(df['day'])
df["day"] = df["day"].dt.strftime("%Y-%m-%d")

# render stats last 30d on day level
st.subheader("Number of disruptions per day")
bars = alt.Chart(df).mark_bar().encode(
        y=alt.Y("day:N", title="Date"),
        x=alt.X("count:Q", stack="zero", title="Number of disruptions"),
        color=alt.Color("type:N", title="Type")
)

# text layer
text = alt.Chart(df).mark_text(dx=-12, dy=0, color="black", baseline="middle").encode(
    y=alt.Y("day:N"),
    x=alt.X("count:Q", stack="zero"),
    detail="type:N",
    text=alt.Text("count:Q")
)

final_chart = bars + text

st.altair_chart(final_chart, use_container_width=True)

# fetch all the data
@st.cache_data
def fetch_data():
    conn = st.connection("postgresql", type="sql")

    df_map_data = conn.query("SELECT * FROM ns.map_data")
    df_24h_stats = conn.query("SELECT * FROM ns.disruptions_24h")
    df_day_stats = conn.query("SELECT * FROM ns.day_aggregations")

    conn.session.close()

    return (df_map_data, df_24h_stats, df_day_stats)



#for row in df_map_data.itertuples():
#    st.write(f"date: {row.station_code}, disruption_count: {row.involved_disruptions}, level: {row.level}, station_type: {row.station_type}, location: {row.location}")