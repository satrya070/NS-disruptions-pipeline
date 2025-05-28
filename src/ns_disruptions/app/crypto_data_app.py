import streamlit as st

st.title("Crypto Data")

# init conn the streamlit way
conn = st.connection("postgresql", type="sql")

df = conn.query("SELECT * FROM public.coins_data")

st.text("showing data..")

for row in df.itertuples():
    st.write(f"{row.name} is at rate: {row.price}")