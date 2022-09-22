import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

gender_map = { 1: 'männlich', 2: 'weiblich', 3: 'divers'}
yn_map = { 0: 'nein', 1: 'ja'}
e_map={4:'stimmt vollkommen', 3: 'stimmt eher', 2:'teils/teils', 1: 'stimmt eher nicht', 0: 'stimmt überhaupt nicht'}
u_map={0:'ja', 1:'ja, vielleicht', 2:'weiss nicht', 3: 'eher nein', 4: 'nein, auf keinen Fall'}

pos_eff = ['e_pain','e_smoking','e_fear','e_memory','e_selfworth','e_anxiety']
neg_eff = ['e_force','e_nowake','e_freewill','e_intelligent']

def transform_data(data):
    data['pos_eff'] = (data['e_pain']+data['e_smoking']+data['e_fear']+data['e_memory']+data['e_selfworth']+data['e_anxiety']) / 6
    data['neg_eff'] = (data['e_force']+data['e_nowake']+data['e_freewill']+data['e_intelligent']) / 4
    data['try'] = data['tryhypnosis']

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

def predjudice_chart(q,questions,squestions,title, tx,ty):
    pred=data[q]
    p_counts = pred.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    p_counts["desc"] = p_counts['index'].map(questions)
    p_counts["sdesc"] = p_counts['index'].map(squestions)
    p_counts=p_counts.fillna(0)
    p_counts_l = p_counts.melt(id_vars=['index', 'desc', 'sdesc'],var_name='answer',value_name='anteil')
    p_counts_l['answer_num'] = p_counts_l['answer'].map({v: k for k, v in e_map.items()})
    color_scale = alt.Scale(
        domain=[
            "stimmt überhaupt nicht",
            "stimmt eher nicht",
            "teils/teils",
            "stimmt eher",
            "stimmt vollkommen"
        ],
        range=["#bb2528", "#ea4630", "#f8b229", "#146b3a", "#165b33"]
    )
    #    range=["#e73c3e", "#ed7172", "#ffd100", "#bce55c", "#97d700"]
    ch = alt.Chart(p_counts_l).mark_bar().encode(
        y=alt.X('sdesc:N', title=tx, axis=alt.Axis(labelAngle=0)),
        x=alt.Y('anteil:Q',title=ty),


        color=alt.Color('answer:N', scale=color_scale, title=tx),
        order=alt.Order(
        # Sort the segments of the bars by this field
        'answer_num',
        sort='ascending'
        )
    ).properties(
        title=title,
    )
    return ch

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
        color=alt.Color('desc:N', title=tx),
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
    ty="Zustimmung"
    tx="Quelle"
    title='Woher ist Ihnen Hypnose bekannt',
    return bars(q, questions,squestions,title,tx,ty)


def type_chart ():
    q = ['t_selfhypnosis', 't_show', 't_medical', 't_mindreading']
    questions = {
        't_selfhypnosis':'Selbsthypnose',
        't_show':'Showhypnose',
        't_medical': 'medizinische Hypnose',
        't_mindreading': 'Mindreading',
    }
    squestions = {
        't_selfhypnosis':'Selbsthypnose',
        't_show':'Showhypnose',
        't_medical': 'Hypnotherapie',
        't_mindreading': 'Mindreading',
    }
    title='Welche Arten von Hypnose sind Ihnen bekannt?',
    tx='Hypnoseart'
    ty='Bekanntheit'
    return bars(q, questions,squestions,title,tx,ty)


def pospred_graph():
    q = pos_eff
    questions = {
        'e_pain':'Schmerztheraie',
        'e_smoking':'Rauchentwöhung',
        'e_fear': 'Angsttherapie',
        'e_memory': 'Erinnerungs',
        'e_selfworth': 'Selbstwertsteigerung',
        'e_anxiety': 'Entängstigung'
    }
    squestions = {
        'e_pain':'Schmerztheraie',
        'e_smoking':'Rauchentwöhung',
        'e_fear': 'Angsttherapie',
        'e_memory': 'Erinnerungs',
        'e_selfworth': 'Selbstwertsteigerung',
        'e_anxiety': 'Entängstigung'
    }    
    tx = 'Hypnosewirkung'
    ty = 'Anteil Antwort'
    title = 'Angenommene Wirkungen von Hypnose'
    return predjudice_chart(q, questions,squestions,title,tx,ty)

def negpred_graph():
    q = neg_eff
    questions = {
        'e_force':'Durch Hypnose kann ich gezwungen werden, etwas gegen meinen freien Willen zu tun',
        'e_nowake':'Nach einer Hypnose kann man eventuell nicht mehr wach werden',
        'e_freewill': 'Hypnose kann meinen Willen beeinflussen',
        'e_intelligent': 'Hypnose wirkt bei intelligenten Menschen nicht',
    }
    squestions = {
        'e_force':'Gegen eigenen Willen',
        'e_nowake':'Nicht erwachen',
        'e_freewill': 'Willen beeinflussen',
        'e_intelligent': 'Intelligenzabhängigkeit',
    }


    tx = 'Unerwünschte Wirkung'
    ty = 'Anteil Antwort'
    title = 'Angenommene negative Effekte von Hypnose'
    return predjudice_chart(q, questions,squestions,title,tx,ty)

def use_graph():
    quest = data[['tryhypnosis']]
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).reset_index()
    q_counts['answer_num'] = q_counts['index'].map({v: k for k, v in u_map.items()})
    color_scale = alt.Scale(
        domain=['nein, auf keinen Fall','eher nein','weiss nicht','ja, vielleicht','ja'],
        range=["#bb2528", "#ea4630", "#f8b229", "#146b3a", "#165b33"]
    )
    base = alt.Chart(q_counts).encode(
        x=alt.X('index:N', title='Antwort', axis=alt.Axis(labelAngle=0), sort=alt.EncodingSortField(field="answer_num", order='ascending')),
        y=alt.Y('tryhypnosis:Q', scale=alt.Scale(domain=[0, 1.0]), title='Anteil'),
    ).properties(
        title='Würden Sie Hypnose nutzen?',
    )
    bar = base.mark_bar().encode(
        color=alt.Color('index:N', title='Antwort', scale=color_scale),
    )
    return bar

def use_don():
    quest = data[['tryhypnosis']]
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).transpose().reset_index()
    q_counts = quest.apply(lambda x: x.value_counts(normalize=True)).reset_index()
    q_counts['answer_num'] = q_counts['index'].map({v: k for k, v in u_map.items()})
    color_scale = alt.Scale(
        domain=['nein, auf keinen Fall','eher nein','weiss nicht','ja, vielleicht','ja'],
        range=["#bb2528", "#ea4630", "#f8b229", "#146b3a", "#165b33"]
    )
    base = alt.Chart(q_counts).encode(
        theta=alt.Theta("tryhypnosis:Q",
            stack=True, 
            scale=alt.Scale(type="linear",rangeMax=1.5708, rangeMin=-1.5708),
            sort=alt.EncodingSortField(field="answer_num", order='ascending'),
        ),
        color=alt.Color(field="index", type="nominal",scale=color_scale),
    )
    pie = base.mark_arc(innerRadius=75).encode(
    )
    text = base.mark_text(radius=170, innerRadius=75, fontSize=16).encode(
        text=alt.Text('tryhypnosis:Q', format='0.2f'),
        color=alt.value('black')
    )
    return pie+text

def correlation_chart():
    ch = alt.Chart(data, height=300, width=300).mark_point().encode(
        y=alt.X('try:N', title='Zustimmung',sort=alt.EncodingSortField(field="try", order='ascending' )),
        x=alt.Y('pos_eff:Q', scale=alt.Scale(domain=[0, 4.0]), title='Mean'),
        color="gender:N"
    ).properties(
        title="Positive Vorurteile"
    )
    cch = ch + ch.transform_regression('pos_eff','try').mark_line()

    ch2 = alt.Chart(data, height=300, width=300).mark_point().encode(
        y=alt.X('try:N', title='Zustimmung',sort=alt.EncodingSortField(field="try", order='ascending' )),
        x=alt.Y('neg_eff:Q', scale=alt.Scale(domain=[0, 4.0]), title='Mean'),
        color="gender:N"
    ).properties(
        title="Negative Vorurteile"
    )
    cch2 = ch2 + ch2.transform_regression('neg_eff','try').mark_line()

    return cch | cch2



st.title('Umfrage Vorurteile Hypnose')
st.subheader('Stichprobe')
st.write(data)
st.subheader('Verteilung Geschlecht')
st.altair_chart(gender_chart(),use_container_width=True)
st.subheader('Woher ist Hypnose bekannt?')
st.altair_chart(qcount_chart(),use_container_width=True)
st.subheader('Welche Arten von Hypnose sind Ihnen bekannt?')
st.altair_chart(type_chart(),use_container_width=True)
st.subheader('Positive Vorurteile')
st.altair_chart(pospred_graph(),use_container_width=True)
st.subheader('Negative Vorurteile')
st.altair_chart(negpred_graph(),use_container_width=True)
st.subheader('Würden Sie Hypnose nutzen')
st.altair_chart(use_graph(),use_container_width=True)
st.altair_chart(use_don(),use_container_width=True)
st.subheader('Korrelation')
st.altair_chart(correlation_chart(),use_container_width=True)