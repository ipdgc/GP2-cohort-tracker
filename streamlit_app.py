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


df=pd.read_csv('Data Curation - OCT 2021 - CLEANED_DATA.csv')
df['Current_Total'].fillna(df.Current_Total, inplace=True)
df_count_country = df.groupby('Main_Site')['Short_Name'].count()
df['Timestamp'] = pd.to_datetime(df['Timestamp'],format='%m/%d/%Y', errors='ignore')
countries = df['Main_Site'].unique()

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
    total_n = df['Current_Total'].sum()   
    st.markdown(total_n)
with head_4:
    st.markdown("LAST UPDATED")
    st.markdown("October 2021")


########################  SIDE BAR #########################################

st.sidebar.markdown('**Find your cohort**', unsafe_allow_html=True)
countries_selected = st.sidebar.multiselect('Countries', countries)

if len(countries_selected) > 0:

    df_cf = df.loc[df['Main_Site'].isin(countries_selected)]
else:
    df_cf = df


slider_1, slider_2 = st.sidebar.slider('Cohort size',int(df_cf['Current_Total'].min()),int(df_cf['Current_Total'].max()+1),[int(df_cf['Current_Total'].min()),int(df_cf['Current_Total'].max()+1)],10)

        
df_csf = df_cf[df_cf['Current_Total'].between(slider_1, slider_2)].reset_index(drop=True)


cohort_selection = st.sidebar.selectbox('Cohort selection',df_csf['Short_Name'].unique())
df_selected = df_csf.loc[df_csf['Short_Name'] == cohort_selection]
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
       df_map = df.loc[df['Continent'] == 'Europe']

ASIA = asia.button('ASIA/OCEANIA')
if ASIA:
    with asia:
       df_map = df.loc[df['Continent'] == 'Asia/Oceania']

NAM = na.button('NORTH AMERICA')
if NAM:
    with na:
       df_map = df.loc[df['Continent'] == 'North America']

SAM = sa.button('SOUTH AMERICA')
if SAM:
    with sa:
       df_map = df.loc[df['Continent'] == 'South America']


########################  2nd row   #########################################
left_column, right_column = st.beta_columns([2.5,1])
with right_column:
    df_selected_update = df_selected[['Proposed_Samples_by2022', 'Processed_Samples']]
    st.markdown(df_selected['Short_Name'][0])
    st.table(df_selected_update.assign(hack='').set_index('hack'))
    ppd=df_selected['Current_PD']
    nonpd=df_selected['Current_nonPD']
    d=pd.concat([ppd, nonpd], axis = 1).T
    d.columns = ['cohort']
    fig = px.pie(d, values=d['cohort'], names = d.index, title = "PD/nonPD")
    fig.update_layout(showlegend=False,
		width=300,
		height=300)
    st.write(fig)
    st.markdown("**Study Name**")
    st.write(df_selected['Full_Name'][0])
    st.markdown("**Main Study Site**")
    st.write(df_selected['City/State'][0])
    st.markdown("**Cohort completion year**")
    st.write(df_selected['Cohort_completion_Year'][0])
    st.markdown("**Is cohort multisite?**")
    st.write(df_selected['Multisite_Study'][0])
    st.markdown("**Patient Type**")
    st.write(df_selected['Participant_type'][0])
    st.markdown("**Study type**")
    st.write(df_selected['Study_type'][0])
   
with left_column:
    df_map['cohort_number'] = df_map.groupby('Main_Site')['Short_Name'].transform('size')
    geo_map = px.scatter_geo(df_map, locations="Main_Site", color=np.log10(df_map['Current_Total']),
                     hover_name="Main_Site", size = 'cohort_number',
                     projection="natural earth", color_continuous_scale = px.colors.sequential.Plasma, 
                     locationmode = "country names")
    geo_map.update_layout(title_text = "GP2 Cohort Participant Numbers Geo Scatter Map",
		width=1000,
		height=700)
    geo_map.update_coloraxes(colorbar_title = "Log10 Pat#",colorscale = "deep", reversescale=False)
    st.write(geo_map)




#with left_column:
#    cho_map = px.choropleth(df_map, locations = "Main_Site",
#                    color = np.log10(df_map['Current_Total']), 
#                    hover_name = "Main_Site", 
#                    hover_data = ["Current_Total", 'Short_Name'],
#                    color_continuous_scale = px.colors.sequential.Plasma, locationmode = "country names")
#    cho_map.update_layout(title_text = "GP2 Cohort Participant Numbers Choropleth Map",
#		width=1000,
#		height=700)
#    cho_map.update_coloraxes(colorbar_title = "Log10 Pat#",colorscale = "deep", reversescale=False)
#    st.write(cho_map)

