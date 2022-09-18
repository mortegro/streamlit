import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

gender_map = { 1: 'männlich', 2: 'weiblich', 3: 'divers'}
yn_map = { 0: 'nein', 1: 'ja'}
e_map={4:'stimmt vollkommen', 3: 'stimmt eher', 2:'teils/teils', 1: 'stimmt eher nicht', 0: 'stimmt überhaupt nicht'}
u_map={0:'ja', 1:'ja, vielleicht', 2:'weiss nicht', 3: 'eher nein', 4: 'nein, auf keinen Fall'}

def transform_data(data):
    data.gender = data.gender.map(gender_map).astype("category")
    data.knowhypnosis = data.knowhypnosis.map(yn_map).astype("category")
    data.q_books = data.q_books.map(yn_map).astype("category")
    data.q_internet = data.q_internet.map(yn_map).astype("category")
    data.q_film = data.q_film.map(yn_map).astype("category")
    data.q_personal = data.q_personal.map(yn_map).astype("category")
    data.q_friends = data.q_friends.map(yn_map).astype("category")

    data.t_selfhypnosis = data.t_selfhypnosis.map(yn_map).astype("category")
    data.t_show = data.t_show.map(yn_map).astype("category")
    data.t_medical = data.t_medical.map(yn_map).astype("category")
    data.t_mindreading = data.t_mindreading.map(yn_map).astype("category")

    data.e_pain = data.e_pain.map(e_map).astype("category")
    data.e_smoking = data.e_smoking.map(e_map).astype("category")
    data.e_fear = data.e_fear.map(e_map).astype("category")
    data.e_memory = data.e_memory.map(e_map).astype("category")
    data.e_selfworth = data.e_selfworth.map(e_map).astype("category")
    data.e_anxiety = data.e_anxiety.map(e_map).astype("category")
    
    data.e_force = data.e_force.map(e_map).astype("category")
    data.e_nowake = data.e_nowake.map(e_map).astype("category")
    data.e_freewill = data.e_freewill.map(e_map).astype("category")
    data.e_intelligent = data.e_intelligent.map(e_map).astype("category")

    data.tryhypnosis = data.tryhypnosis.map(u_map).astype("category")
    return data


data = transform_data (pd.read_excel('umfrage.xlsx'))

def gender_chart():
    base = alt.Chart(data).encode(
        theta=alt.Theta('count(gender):Q',stack=True),
        color='gender:N'
    ).properties(
        title = "Geschlecht der Stichprobe (n=60)"
    )

    arc = base.mark_arc(radius=120).encode(
        color='gender:N'
    )

    text = base.mark_text(radius = 140, size=20).encode(
        text='count(gender):Q'
    )

    return (arc+text)


def bars(q,questions,squestions,title, tx,ty):
    quest = data[q]
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    q_counts["desc"] = q_counts['index'].map(questions)
    q_counts["sdesc"] = q_counts['index'].map(squestions)
    base = alt.Chart(q_counts).encode(
        x=alt.X('sdesc:N', title=tx, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('ja', scale=alt.Scale(domain=[0, 1.0]), title=ty)
    ).properties(
        title=title,
    )
    bar = base.mark_bar().encode(
        color=alt.Color('desc:N', title="Quelle"),
    )
    return bar


def qcount_chart():
    q = ['q_books', 'q_internet', 'q_film', 'q_personal', 'q_friends']
    questions = {
        'q_books':'Aus Büchern',
        'q_internet':' Aus dem Internet',
        'q_film': 'Aus Film/Fernsehen',
        'q_personal': 'persönliche Erfahrung',
        'q_friends': 'durch Freunde',
    }
    squestions = {
        'q_books':'Bücher',
        'q_internet':'Internet',
        'q_film': 'Medien',
        'q_personal': 'selbst',
        'q_friends': 'Freunde',
    }
    quest = data[q]
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    q_counts["desc"] = q_counts['index'].map(questions)
    q_counts["sdesc"] = q_counts['index'].map(squestions)
    base = alt.Chart(q_counts).encode(
        x=alt.X('sdesc:N', title="Vorurteil", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('ja', scale=alt.Scale(domain=[0, 1.0]), title="Zustimmung")
    ).properties(
        title='Woher ist Ihnen Hypnose bekannt',
    )
    bar = base.mark_bar().encode(
        color=alt.Color('desc:N', title="Quelle"),
    )
    text = base.mark_text(size=15, clip=False, dy=+10).encode(
        text='sdesc',
    )
    return (bar )


def type_chart ():
    q = ['t_selfhypnosis', 't_show', 't_medical', 't_mindreading']
    quest = data[q]
    questions = {
        't_selfhypnosis':'Selbsthypnose',
        't_show':'Showhypnose',
        't_medical': 'medizinische Hypnose',
        't_mindreading': 'Mindreading',
    }
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    q_counts["desc"] = q_counts['index'].map(questions)
    bar = alt.Chart(q_counts).mark_bar().encode(
        x=alt.X('desc:N', title="Hypnoseart", axis=alt.Axis(labelAngle=0)),
        y=alt.Y('ja', scale=alt.Scale(domain=[0, 1.0]), title="Bekanntheit"),
        color=alt.Color('desc:N', title="Quelle"),
    ).properties(
        title='Woher ist Ihnen Hypnose bekannt',
    )
    return (bar)



st.title('Umfrage Vorurteile Hypnose')
st.subheader('Stichprobe')
st.write(data.head())
st.subheader('Verteilung Geschlecht')
st.altair_chart(gender_chart(),use_container_width=True)
st.subheader('Woher ist Hypnose bekannt?')
st.altair_chart(qcount_chart(),use_container_width=True)
st.subheader('Welche Arten von Hypnose sind Ihnen bekannt?')
st.altair_chart(type_chart(),use_container_width=True)
st.subheader('Positive Vorurteile')


st.subheader('Negative Vorurteile')

