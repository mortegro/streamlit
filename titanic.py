import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


titanic = pd.read_csv('https://raw.githubusercontent.com/jorisvandenbossche/pandas-tutorial/master/data/titanic.csv')
st.markdown("""
# Titanic

""")

st.write(titanic)
st.write(titanic.describe())

c = alt.Chart(titanic,width=800,height=600).mark_point().encode(
    x='Age:Q',
    y='Fare:Q',
    color='Pclass:N',
    tooltip=['Name', 'Age', 'Fare', 'Sex'],
    shape='Survived:N'
).interactive()

st.altair_chart(c)