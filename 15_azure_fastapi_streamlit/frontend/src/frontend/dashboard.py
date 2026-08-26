import streamlit as st
import httpx
import pandas as pd
import os 

BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def main():
    st.markdown("# PokeDash")

    st.write(BASE_URL)

    stats = httpx.get(f"{BASE_URL}/pokemons/stats").json()

    st.markdown("All cool stuffs u need 2 know abt pokes")

    st.markdown("## PokeTypes")
    pokemons_per_type = httpx.get(f"{BASE_URL}/pokemons/number_types").json()

    pokemons_per_type = pd.DataFrame(
        list(pokemons_per_type.items()), columns=["type", "number"]
    )
    st.bar_chart(pokemons_per_type.head(8), x="type", y="number")

    st.dataframe(stats)

    df = pd.DataFrame(stats)
    types = df["Type 1"].unique()
    poke_type = st.selectbox(label="Choose pokemon type", options=types)

    poke_types = httpx.get(f"{BASE_URL}/pokemons/type?poke_type={poke_type}").json()

    st.dataframe(poke_types)

    st.markdown("Pokemon stats")

if __name__ == "__main__":
    main()