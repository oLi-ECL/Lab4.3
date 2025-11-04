import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px
import altair as alt

#import kagglehub


#path = kagglehub.dataset_download("paperxd/all-computer-prices")
path = 'computer_prices_all.csv'
df = pd.read_csv(path)
df = df[['device_type','brand', 'model', 'release_year', 'os', 'cpu_brand', 'cpu_model','gpu_brand', 'gpu_model',
    'ram_gb', 'storage_type', 'storage_gb','storage_drive_count', 'display_type', 'display_size_in', 'resolution',
       'refresh_hz', 'battery_wh', 'price']]
#print(laptop_data.columns)
alt.themes.enable("dark")

laptop_data = df[df['device_type'] == 'Laptop']
brand_counts = laptop_data['brand'].value_counts()

st.set_page_config(
    page_title="Computer Laptop Sales Data",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded")

with st.sidebar:
    st.title('Laptop Sales Data')
    
    year_list = sorted(list(laptop_data['release_year'].unique()))
    selected_year = st.selectbox('Select Year', year_list, index=len(year_list)-1)

    
    #Brand_select = st.selectbox('Select Brand', list(laptop_data['brand'].unique()))
    #brand_data = laptop_data[laptop_data['brand'].isin(Brand_select)]
    #brand_c = brand_data['cpu_model', 'gpu_model', 'display_type', 'storage_type'].value_counts().reset_index()
    
    #list_Display =  ['Brand','CPU', 'GPU', 'Display']
    #selected_Category = st.selectbox('Select a Category', list_Display)


    #taken from https://github.com/dataprofessor/population-dashboard
def make_donut(input_response, input_text, input_color):
  
    if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
    source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
    source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
    return plot_bg + plot + text
  

def make_bar(data):
   df_bar = data.groupby('brand').size().reset_index(name='counts')
   bar = alt.Chart(df_bar).mark_bar().encode(
        x=alt.X('brand:N', sort='-y', title='Brand'),
        y=alt.Y('counts:Q', title='Number of Laptops'),
        color = alt.Color('brand:N', title='Brand'),
        tooltip=['brand', 'counts']
    ).properties(width=600, height=400)
   return bar   


#----------------------------------------------------------
col = st.columns((5, 2, 2), gap='medium')

laptop_year = laptop_data[laptop_data['release_year'] == selected_year]

with col[0]:
    st.markdown(f'Number of Laptops Brand Released in {selected_year}')
    bar_chart = make_bar(laptop_year)
    st.altair_chart(bar_chart)
    
#with col[0]:
   #st.write(brand_c.head(10))

with col[1]:
    st.markdown('CPU Distribution')
    gpu_counts = laptop_year['cpu_brand'].shape[0]
    Intel_count = laptop_year[laptop_year['cpu_brand'] == 'Intel'].shape[0]
    AMDc_count = laptop_year[laptop_year['cpu_brand'] == 'AMD'].shape[0]

    Intel_donut = make_donut(round(Intel_count/gpu_counts * 100), 'Intel', 'blue')
    AMDc_donut = make_donut(round(AMDc_count/gpu_counts * 100), 'AMD', 'red')
    
    double_rowc = st.columns((.2,1,.2))

    with double_rowc[1]:
        st.write('Intel')
        st.altair_chart(Intel_donut)
        st.write('AMD')
        st.altair_chart(AMDc_donut)


with col[2]:
    st.markdown('GPU Distribution')
    gpu_counts = laptop_year['gpu_brand'].shape[0]
    Nvidia_count = laptop_year[laptop_year['gpu_brand'] == 'NVIDIA'].shape[0]
    AMD_count = laptop_year[laptop_year['gpu_brand'] == 'AMD'].shape[0]

    Nvidia_donut = make_donut(round(Nvidia_count/gpu_counts * 100), 'Nvidia', 'green')
    AMD_donut = make_donut(round(AMD_count/gpu_counts * 100), 'AMD', 'red')
    
    double_row = st.columns((.2,1,.2))

    with double_row[1]:
        st.write('Nvidia')
        #st.write(Nvidia_count/gpu_counts * 100)
        st.altair_chart(Nvidia_donut)
        st.write('AMD')
        st.altair_chart(AMD_donut)

with st.container():
    st.markdown('Insights')
    st.write("The main thing is guess it I have a lot of data but don't know what to do with it.")
    st.write("It's just what question can I answer with this data.")
    st.write("I had a idea of a second multiselect box to select brand and the top parts but displaying the with graphs would be difficult.")
    st.write('Another idea was if brands changed between using more AMD cpus.')


 