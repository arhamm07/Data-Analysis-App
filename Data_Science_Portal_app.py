# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from plotly.subplots import make_subplots


st.set_page_config(page_title="Data Science Portal", page_icon="🧊", layout="wide")


st.title("Data Science Portal")


st.subheader(":grey[Welcome to the Data Science Portal. This is a platform for data scientists to share their work and collaborate with others.] " , divider = 'rainbow')

file = st.file_uploader("Upload your file", type = ["csv", "xlsx"])

if file is not None:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        st.error("Invalid file type")
        st.stop()
    st.dataframe(df)
    st.success("File uploaded successfully")

    st.subheader(":grey[Basic Information of Data]" , divider = 'rainbow')
    tab1, tab2, tab3 , tab4 = st.tabs(["Summary", "Head and Tail", "Data Types", "Columns"])


    with tab1:
        st.write("There are total :red[", df.shape[0], "] rows and :red[", df.shape[1], "] columns in the dataset.")
        st.subheader(":grey[Summary of Data]")
        st.write(df.describe())

    with tab2:
        st.subheader(":grey[Top Rows]")
        top_rows = st.slider("Select the number of rows to display", min_value=1, max_value=20 ,key = "top_rows")
        st.dataframe(df.head(top_rows))

        st.subheader(":grey[Bottom Rows]")
        bottom_rows = st.slider("Select the number of rows to display", min_value=1, max_value=20 ,key = "bottom_rows")
        st.dataframe(df.tail(bottom_rows))

    with tab3:
        st.subheader(":grey[Data Types]")
        st.write(df.dtypes)
    
    
    with tab4:
        st.subheader(":grey[Columns]")
        st.write(list(df.columns))

    st.subheader(":grey[Choose Columns to Count Values]" , divider = 'rainbow')
    with st.expander("Value Counts"):
        col1, col2 = st.columns(2)
        with col1:
            selected_columns = st.multiselect("Select Columns", list(df.columns))
        with col2:
            top_n = st.number_input("Select the number of values to display", min_value=1, max_value=20, step=1)

        if st.button("Display"):
                if selected_columns:
                    result = df[selected_columns].value_counts().head(top_n)
                    st.write(result)
                    st.subheader(":grey[Visualization]")
                    
                    # Convert MultiIndex to a list of tuples
                    index_tuples = list(result.index)
                    
                    # Create a DataFrame from the result
                    result_df = pd.DataFrame({
                        'Count': result.values,
                        'Category': [' - '.join(map(str, tup)) for tup in index_tuples]
                    })
                    
                    fig = px.bar(result_df, x='Category', y='Count', color='Category', title="Bar Chart")
                    st.plotly_chart(fig, use_container_width=True)
                    fig = px.pie(result_df, names='Category', values='Count', title="Pie Chart")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No columns selected")   
        


    st.subheader(":grey[Simplify Your Data Analysis]" , divider = 'rainbow')
    col1, col2, col3 = st.columns(3)
    with col1:
        groupby_column = st.multiselect("Select a column to group by",options= list(df.columns))
    with col2:
        operation_column = st.selectbox("Select an operation column", options= list(df.columns))
    with col3:
        operation = st.selectbox("Select an operation", options= ["mean", "median", "mode", "sum", "min", "max" , "std","size","count"])

    result = df.groupby(groupby_column).agg(
        new_col = (operation_column, operation)
    ).reset_index()

    st.dataframe(result)

        
    st.subheader(":grey[Data Visualization]", divider='rainbow')
    graph_type = st.selectbox("Select the type of graph", options=["Line", "Bar", "Scatter", "Sunburst", "Pie" , "Box" , "Histogram"])
    
    if graph_type == "Line":
        x_axis = st.selectbox("Select the x-axis", options=list(result.columns))
        y_axis = st.selectbox("Select the y-axis", options=list(result.columns))
        color_column = st.selectbox("Select the color column", options=[None] + list(result.columns))
        fig = px.line(result, x=x_axis, y=y_axis, color=color_column, markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "Pie":
        values = st.selectbox("Select the values",options= list(result.columns))
        names = st.selectbox("Select the names",options= list(result.columns))
        fig = px.pie(result, values=values, names=names)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "Bar":
        x_axis = st.selectbox("Select the x-axis",options= list(result.columns))
        y_axis = st.selectbox("Select the y-axis",options= list(result.columns))
        color_column = st.selectbox("Select the color column", options=[None] + list(result.columns))
        facet_column = st.selectbox("Select the facet column", options=[None] + list(result.columns))
        fig = px.bar(result, x=x_axis, y=y_axis, color=color_column, facet_col=facet_column , barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "Sunburst":
        path_columns = st.multiselect("Select the path columns", options=list(result.columns))
        if path_columns:
            fig = px.sunburst(result, path=path_columns , values='new_col')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("Please select at least one path column for the Sunburst Chart.")
    
    elif graph_type == "Scatter":
        x_axis = st.selectbox("Select the x-axis",options= list(result.columns))    
        y_axis = st.selectbox("Select the y-axis",options= list(result.columns))
        color_column = st.selectbox("Select the color column", options=[None] + list(result.columns))
        size_column = st.selectbox("Select the size column", options=[None] + list(result.columns))
        fig = px.scatter(result, x=x_axis, y=y_axis, color=color_column, size=size_column)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "Box":
        x_axis = st.selectbox("Select the x-axis",options= list(result.columns))    
        fig = px.box(result, x=x_axis)
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_type == "Histogram":
        x_axis = st.selectbox("Select the column",options= list(result.columns))    
        color_column = st.selectbox("Select the color column", options=[None] + list(result.columns))
        fig = px.histogram(result, x=x_axis, color=color_column, hover_data=result.columns , opacity=0.65)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No graph type selected")