import streamlit as st


def build_grid():
        for i in range(int(grid_size)):
            i = st.columns(3, gap=None, border=True)


grid_size = st.number_input("Enter Grid Size: ", value=None, placeholder = "Type a number...")
st.button("Build grid", on_click = build_grid)

