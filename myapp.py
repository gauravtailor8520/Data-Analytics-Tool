
import json
import requests  # pip install requests
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
    


st.set_page_config(
    page_title="Data Visualization Portal",
    page_icon="📈"
)

lottie_hello = load_lottieurl("https://lottie.host/549c98c5-8615-4ff5-8601-4f4e58fae866/5wcyBTbRfI.json")

st_lottie(
    lottie_hello,
    speed=0.5,
    reverse=False,
    loop=True,
    quality="low",  # medium ; high
    
    height=200,  # Adjust the height to your desired size
    width=400,   # Adjust the width to your desired size
    key=None,
)

st.title(':rainbow[Data Analytics Portal]' ,)
st.subheader(':grey[Explore Data with ease.]',divider='rainbow')


file = st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])



if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)   

    st.dataframe(data)     
    st.info('File is successfully Uploaded', icon="🔥")

    st.subheader(':grey[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4 = st.tabs(['summery', 'Top and Bottom Rows', 'Data Types', 'Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data .shape[1]} columns in dataset')
        st.subheader(':grey[Statistical summary of the dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':grey[Top Rows]')
        toprows = st.slider('Number of rows you want',1,data.shape[0],key = 'topslider')
        st.dataframe(data.head(toprows))    

        st.subheader(':grey[Bottom Rows]')
        bottomrows = st.slider('Number of rows you want',1,data.shape[0],key = 'bottomslider')
        st.dataframe(data.tail(bottomrows)) 

    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes) 
    
    with tab4:
        st.subheader(':grey[Column names in Dataset]')
        st.write(list(data.columns))
    
    st.subheader(':grey[Column Values To count]', divider = 'rainbow')

    with st.expander('Value Count'):
        col1,col2 = st.columns(2)

        with col1:
            column = st.selectbox('Chhose Column name', options=list(data.columns))
            
        with col2:
            toprows = st.number_input('Top rows', min_value=1, step=1) 

        count = st.button('count')
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization', divider="grey")

            fig = px.bar(data_frame=result,x=column, y='count', template= 'plotly_white', text = 'count')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result ,x=column, y='count', text='count',template= 'plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column, values="count")
            st.plotly_chart(fig)
        else:
            st.error("Gives you the value count for choosen category.")
    
    st.subheader(':rainbow[Groupby : Simplify your data analysis]', divider = "grey" )
    st.write('The groupby lets you summerize data by specific categories and group')        
    with st.expander('Group By your column '):
        col1,col2,col3 = st.columns(3) 
        with col1:
            groupby_cols = st.multiselect("Choose column to groupby", options= list(data.columns))
        with col2:
            operation_col = st.selectbox("Choose column for operation", options= list(data.columns))
        with col3:
            operation = st.selectbox("Choose operation", options= ['sum','max','min','mean','median', 'count' ])

        if groupby_cols and operation_col:
            if len(groupby_cols) > 0:
                if operation_col in data.columns:
                    if operation in ['sum', 'max', 'min', 'mean', 'median']:
                        if np.issubdtype(data[operation_col].dtype, np.number):
                            try:
                                result = data.groupby(groupby_cols).agg(
                                    newcol=(operation_col, operation)).reset_index()
                                st.dataframe(result)

                                st.subheader(':grey[Data Visualization]', divider='rainbow') 
                                graphs = st.selectbox('Choose your graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])

                                if graphs == 'line':
                                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                    color = st.selectbox('Color information', options=[None] + list(result.columns))
                                    fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color)
                                    st.plotly_chart(fig)
                                
                                elif graphs == 'bar':
                                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                    color = st.selectbox('Color information', options=[None] + list(result.columns))
                                    facet_col = st.selectbox('Column information', options=[None] + list(result.columns))
                                    fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
                                    st.plotly_chart(fig)
                                
                                elif graphs == 'scatter':
                                    x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                    y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                    color = st.selectbox('Color information', options=[None] + list(result.columns))
                                    size = st.selectbox('Size column', options=[None] + list(result.columns))
                                    fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
                                    st.plotly_chart(fig)

                                elif graphs == 'pie':
                                    values = st.selectbox('Choose Numerical Values', options=list(result.columns))
                                    names = st.selectbox('Choose labels', options=list(result.columns))
                                    fig = px.pie(data_frame=result, values=values, names=names)
                                    st.plotly_chart(fig)    

                                elif graphs == 'sunburst':
                                    path = st.multiselect('Choose your path', options=list(result.columns))
                                    if len(path) > 1:
                                        fig = px.sunburst(result, path=path, values='newcol')
                                        st.plotly_chart(fig)
                                    else:
                                        st.warning('Please select at least two columns for the path.')
                            except Exception as e:
                                st.error(f"An error occurred while performing the operation: {e}")
                        else:
                            st.error("The selected column for operation must be numerical for the chosen operation.")
                    elif operation == 'count':
                        try:
                            result = data.groupby(groupby_cols).size().reset_index(name='count')
                            st.dataframe(result)

                            st.subheader(':grey[Data Visualization]', divider='rainbow') 
                            graphs = st.selectbox('Choose your graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])

                            if graphs == 'line':
                                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                color = st.selectbox('Color information', options=[None] + list(result.columns))
                                fig = px.line(data_frame=result, x=x_axis, y='count', color=color)
                                st.plotly_chart(fig)
                            
                            elif graphs == 'bar':
                                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                color = st.selectbox('Color information', options=[None] + list(result.columns))
                                facet_col = st.selectbox('Column information', options=[None] + list(result.columns))
                                fig = px.bar(data_frame=result, x=x_axis, y='count', color=color, facet_col=facet_col, barmode='group')
                                st.plotly_chart(fig)
                            
                            elif graphs == 'scatter':
                                x_axis = st.selectbox('Choose X axis', options=list(result.columns))
                                y_axis = st.selectbox('Choose Y axis', options=list(result.columns))
                                color = st.selectbox('Color information', options=[None] + list(result.columns))
                                size = st.selectbox('Size column', options=[None] + list(result.columns))
                                fig = px.scatter(data_frame=result, x=x_axis, y='count', color=color, size=size)
                                st.plotly_chart(fig)

                            elif graphs == 'pie':
                                values = st.selectbox('Choose Numerical Values', options=['count'])
                                names = st.selectbox('Choose labels', options=list(result.columns))
                                fig = px.pie(data_frame=result, values=values, names=names)
                                st.plotly_chart(fig)    

                            elif graphs == 'sunburst':
                                path = st.multiselect('Choose your path', options=list(result.columns))
                                if len(path) > 1:
                                    fig = px.sunburst(result, path=path, values='count')
                                    st.plotly_chart(fig)
                                else:
                                    st.warning('Please select at least two columns for the path.')
                        except Exception as e:
                            st.error(f"An error occurred while performing the count operation: {e}")
                        else:
                            st.error("The selected column is not numeric.")
                    else:
                        st.error("Invalid operation selected.")
                else:
                    st.error("The selected column is not in the dataset.")
            else:
                st.error("No columns selected for groupby.")
        else:
            st.error("Please select columns for groupby and operation.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
