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
    page_title = 'Cohort Tracker Dashboard',
    layout = 'wide'
)


df=pd.read_csv('df.csv')
df_count_country = df.groupby('Country')['Study'].count()
df_count_group = df.groupby('Group')['Study'].count()

left_column, right_column = st.beta_columns(2)
cohort_selection = st.sidebar.selectbox('Select a cohort',df['Study'])
#cohort_selection = st.sidebar.multiselect('Select a cohort',df.columns)
with right_column:
    st.markdown("**Info for the chosen cohort**")
    cohort = cohort_selection
    st.markdown(f"<h1 style='text-align: center; color: purple;'>{cohort}</h1>", unsafe_allow_html=True)
    cases=df.loc[(df.Study == cohort),['cases']]
    controls=df.loc[(df.Study == cohort),['controls']]
    d=pd.concat([cases, controls], axis = 1).T
    fig = px.pie(d, values=0, names = d.index)
    fig.update_layout(showlegend=False,
		width=200,
		height=200)
    st.write(fig)


cho_map = Image.open('cho_map.png')
left_column.header("GP2 Cohort Map")
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

cohort_pheno = Menu2.button('cohort_pheno')

