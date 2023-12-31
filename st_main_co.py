## Packages

import streamlit as st
import numpy as np
import time
import pandas as pd
import scipy
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import all_functions as af
from PIL import Image

st.set_page_config(page_title="Calcium oscillations analysis tool", layout="wide")

st.sidebar.subheader('File upload')
filepath = st.sidebar.file_uploader('Please upload a valid TTX file')

if filepath:


    # Selecting parameters
    summary_metadata = af.metadata(filepath)
    st.sidebar.dataframe(summary_metadata)

    rawdata = af.rawdata(filepath)

    st.sidebar.subheader('Defining analysis settings')
    threshold = st.sidebar.slider("Select a global detection threshold", min_value=0.01, max_value=0.1, value=0.02,
                                  help='Recommended value 0.02', step=0.005, format="%f")



    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summary of all data", "Display individual well", "Configure plate conditions",
                                      "Configure statistical tests", "Export summary of analysis"])


    with tab1:
        af.all_plotting(rawdata,threshold)
        if st.checkbox("Display rawdata"):
            st.dataframe(data=rawdata['rawdata'])

    with tab2:
        analysiswell = st.selectbox('Type or select well to plot and analyze', rawdata['wells'])
        st.subheader('Plotting well ' + analysiswell)
        af.well_plot(analysiswell, rawdata, threshold, summary_metadata)


    with tab3:
        st.subheader('Specifying wells to compare')
        st.caption("For proping copy/paste functions, prevent Microsoft Edge from blocking Streamlit (click on the right popup dialog within the URL line above)")
        number_of_wells = st.radio("Plate size", [96, 384])

        if number_of_wells == 96:
            rows = 8
            columns = 12
            df = af.template(rows, columns)
            selection = st.data_editor(df)

        else:
            rows = 16
            columns = 24
            df = af.template(rows, columns)
            selection = st.data_editor(df, height=610)




else:
    st.title('To start, select a valid TTX file')
    st.subheader("To exporting a valid TTX file from the FDSS Hamamatsu software, make sure to comply with the following settings:")

    image = Image.open('settings.png')

    st.image(image)
    st.sidebar.write('\n')
    st.sidebar.subheader('Important: due to an unsolved bug, the first attempt for uploading a file will not be successful. '
                         'You must try a second time and upload the same file for proper data parsing.')
    st.sidebar.write('\n')
    st.sidebar.write('\n')
    st.sidebar.write('\n')
    st.sidebar.write('\n')

    st.sidebar.subheader("Clear all Cache Data before analysing a new file")

    if st.sidebar.button("Clear All Cache Data"):
        # Clear values from *all* all in-memory and on-disk data caches:
        st.cache_data.clear()
        st.sidebar.write('Cache has been cleared')

