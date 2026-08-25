import streamlit as st
import httpx 

BASE_URL = "http://127.0.0.1:8000"

def main():
    st.markdown("# PokeDash")

    stats = httpx.get(f"{BASE_URL}/pokemons/stats").json()

    st.dataframe(stats)

    if __name__ == "__main__":
        main()