import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import datetime
import plotly.express as px


st.set_page_config(
    layout = 'wide'
)


df=pd.read_csv('Hackathon_cleaned_data.csv')
df['Total number of study participants'].fillna(df.Total, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df_count_country = df.groupby('Country')['Study'].count()
countries = df['Country'].unique()
df_count_group = df.groupby('Group')['Study'].count()

####################### HEAD ##############################################

head_1, head_2, title, head_3, head_4 = st.beta_columns([1,1,4,1.5,1.5])
mjff = Image.open('mgff_logo.png')
head_1.image(mjff, width = 100)
gp2 = Image.open('gp2_logo.png')
head_2.image(gp2, width = 100)

with title:
    st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">Cohort Tracker Dashboard</p>', unsafe_allow_html=True)

with head_3:
    st.markdown("TOTAL SAMPLES")
    total_n = df['Total number of study participants'].sum()   
    st.markdown(total_n)
with head_4:
    st.markdown("LAST UPDATED")
    most_recent_date = df['Date'].max()   
    st.markdown(most_recent_date)


########################  SIDE BAR #########################################

st.sidebar.markdown('<p class="big-font">Find your cohort</p>', unsafe_allow_html=True)
countries_selected = st.sidebar.multiselect('Countries', countries)

if len(countries_selected) > 0:

    df_cf = df.loc[df['Country'].isin(countries_selected)]
else:
    df_cf = df


slider_1, slider_2 = st.sidebar.slider('Cohort size',int(df_cf['Total number of study participants'].min()),int(df_cf['Total number of study participants'].max()+1),[int(df_cf['Total number of study participants'].min()),int(df_cf['Total number of study participants'].max()+1)],10)

        
df_csf = df_cf[df_cf['Total number of study participants'].between(slider_1, slider_2)].reset_index(drop=True)


cohort_selection = st.sidebar.selectbox('Cohort selection',df_csf['Study'].unique())
df_selected = df_csf.loc[df_csf['Study'] == cohort_selection]
df_selected = df_selected.reset_index()


########################  1st row   #########################################
world, europe, asia, na, sa, aust, blank = st.beta_columns([1,1,1,1,1,1,4])

df_map = df
WORLD = world.button('WORLD')
if WORLD:
    with world:
       df_map = df

EUR = europe.button('EUROPE')
if EUR:
    with europe:
       df_map = df.loc[df['map_filter'] == 'Europe']

ASIA = asia.button('ASIA')
if ASIA:
    with asia:
       df_map = df.loc[df['map_filter'] == 'Asia']

NAM = na.button('NORTH AMERICA')
if NAM:
    with na:
       df_map = df.loc[df['map_filter'] == 'North America']

SAM = sa.button('SOUTH AMERICA')
if SAM:
    with sa:
       df_map = df.loc[df['map_filter'] == 'South America']

AUST = aust.button('AUSTRALIA')
if AUST:
    with aust:
       df_map = df.loc[df['map_filter'] == 'Australia']

########################  2nd row   #########################################
left_column, right_column = st.beta_columns([2.5,1])
with right_column:
    st.markdown(df_selected['Study'][0])
    cases=df_selected['PD Cases']
    controls=df_selected['Controls']
    d=pd.concat([cases, controls], axis = 1).T
    d.columns = ['cohort']
    fig = px.pie(d, values=d['cohort'], names = d.index, title = "Cases/Controls")
    fig.update_layout(showlegend=False,
		width=300,
		height=300)
    st.write(fig)
    st.markdown("**Study Name**")
    st.write(df_selected['Full Name of Study'][0])
    st.markdown("**Main Study Site**")
    st.write(df_selected['City'][0])
    st.markdown("**Patient Type**")
    st.write(df_selected['Who are the participants?'][0])
    st.markdown("**Additional Information**")
    st.write(df_selected['Study Type'][0])
   
with left_column:
    cho_map = px.choropleth(df_map, locations = "Country",
                    color = np.log10(df_map['Total number of study participants']), 
                    hover_name = "Country", 
                    hover_data = ["Total number of study participants", 'Study'],
                    color_continuous_scale = px.colors.sequential.Plasma, locationmode = "country names")
    cho_map.update_layout(title_text = "GP2 Cohort Participant Numbers Choropleth Map",
		width=1100,
		height=770)
    cho_map.update_coloraxes(colorbar_title = "Log10 Participant Numbers",colorscale = "deep", reversescale=False)
    st.write(cho_map)
    st.slider('Timeline', datetime.date(2021,1,1))
