import streamlit as st

st.title("NS disruptions")

# init conn the streamlit way
conn = st.connection("postgresql", type="sql")

df_24h_stats = conn.query("SELECT * FROM ns.disruptions_24h")

df_day_stats = conn.query("SELECT * FROM ns.day_aggregations")

st.text("showing data..")

for row in df_24h_stats.itertuples():
    st.write(f"date: {row.fetch_date}, disruption: {row.id}, is at rat: {row.station_code}")