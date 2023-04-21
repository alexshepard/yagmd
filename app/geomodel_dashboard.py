import streamlit as st
import pandas as pd
import pydeck as pdk

st.sidebar.title("Yet Another Geo Model Dashboard")

taxonomy = pd.read_csv("data/taxonomy.csv")

dashboard_taxa = [
    116840,
    14068,
    210356,
    4924,
    792981,
    13856,
    14161,
    27214,
    556656,
]

show_taxonomy = st.checkbox("Show Taxonomy Dataframe")
if show_taxonomy:
    st.write(taxonomy)

dashboard_taxa_map = {
    t: taxonomy[taxonomy.taxon_id == t]["name"].iloc[0] for t in dashboard_taxa
}

datasets = [
    "presence_maps",
    "env_maps",
    "taxon_range_maps",
]

datasets_names_map = {
    "presence_maps": "Presence",
    "env_maps": "Environmental",
    "taxon_range_maps": "Taxon Range",
}

dataset = st.sidebar.radio(
    "Dataset",
    datasets,
    index=0,
    format_func=lambda x: datasets_names_map[x],
)

taxon_id = st.sidebar.radio(
    "Taxon",
    dashboard_taxa,
    index=0,
    format_func=lambda x: dashboard_taxa_map[x],
)

df = pd.read_json(
    "data/{}/{}.json".format(dataset, taxon_id),
    orient="index",
)
df = df.reset_index()
df.columns = ["hex", "presence"]

threshold = st.sidebar.slider("threshold", 0.0, 1.0, 0.3)
df = df[df.presence > threshold]

layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_hexagon="hex",
    get_fill_color="[90, 255 - (presence * 255), 90]",
    get_line_color="[60, 190 - (presence * 190), 60]",
    line_width_min_pixels=2,
)
r = pdk.Deck(
    map_style="light",
    layers=[layer],
)
st.pydeck_chart(r)
