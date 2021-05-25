import streamlit as st
import pandas as pd
import numpy as np 
#import streamlit.components.v1 as components
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
from PIL import Image
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

#HtmlFile = open("cho_map.html", 'r', encoding='utf-8')
##source_code = HtmlFile.read() 
#components.html(source_code, scrolling=True)

st.set_page_config(
    layout = 'wide'
)


df=pd.read_csv('df.csv')
df['Date'] = pd.to_datetime(df['Date'])
df_count_country = df.groupby('Country')['Study'].count()
df_count_group = df.groupby('Group')['Study'].count()

## HEAD #########################################################

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
    total_n = df['Total_number'].sum()   
    st.markdown(total_n)
with head_4:
    st.markdown("LAST UPDATED")
    most_recent_date = df['Date'].max()   
    st.markdown(most_recent_date)

### CENTER #######################################################

left_column, right_column = st.beta_columns([2.5,1])
cohort_selection = st.sidebar.selectbox('Select a cohort',df['Study'].unique())

cohort_selection1 = st.sidebar.multiselect('Select a cohort',df.columns)
with right_column:
    st.markdown("**Info for the chosen cohort**")
    st.markdown(f"<h1 style='text-align: center; color: purple;'>{cohort_selection}</h1>", unsafe_allow_html=True)
    cases=df['cases'].loc[df['Study'] == cohort_selection]
    controls=df['controls'].loc[df['Study'] == cohort_selection]
    d=pd.concat([cases, controls], axis = 1).T
    d.columns = ['cohort']
    st.write(d)
    fig = px.pie(d, values=d['cohort'], names = d.index)
    fig.update_layout(showlegend=False,
		width=300,
		height=300)
    st.write(fig)


cho_map = Image.open('cho_map.png')
left_column.image(cho_map, use_column_width=True)

Slide, Menu1, Menu2, cohort_pheno = st.beta_columns([4,1,1,2])

with Slide:
    st.slider('Timeline', datetime.date(2021,1,1)) 
Group = Menu1.button('Group')
if Group:
    with Menu1:
       group = st.selectbox('',df_count_group.index)

Country = Menu2.button('Country')
if Country:
    with Menu2:
       country = st.selectbox('',df_count_country.index)
