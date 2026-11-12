import streamlit as st



row1 = st.columns(3, gap=None ,border=True)
row2 = st.columns(3, gap=None ,border=True)
row3 = st.columns(3, gap=None ,border=True)

for col in row1 + row2 + row3:
    tile = col.container(height=120)

    