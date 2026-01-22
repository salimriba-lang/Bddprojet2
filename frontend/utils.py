import streamlit as st
import pandas as pd
import plotly.express as px

def afficher_table(df, titre="Tableau"):
    st.subheader(titre)
    st.dataframe(df)

def afficher_graph(df, x, y, titre="Graphique"):
    fig = px.bar(df, x=x, y=y, text=y)
    fig.update_layout(title=titre, xaxis_title=x, yaxis_title=y)
    st.plotly_chart(fig, use_container_width=True)

def afficher_cards(stats: dict):
    cols = st.columns(len(stats))
    for i, (key, value) in enumerate(stats.items()):
        cols[i].metric(label=key, value=value)
