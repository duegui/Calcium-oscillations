import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time

@st.cache_data
def metadata(filepath):

    # Importing metadata
    metadata = pd.read_csv(filepath, delimiter='\t', nrows=6, header=None, index_col=1)
    metadata = metadata.drop(columns=[0])
    metadata = metadata[2].to_dict()

    acquisition_date = pd.to_datetime(metadata['Date :'])
    acquisition_time = pd.to_timedelta(metadata['Time :'])

    marker = pd.to_timedelta(metadata['Marker1 :'])
    markerint = marker / pd.Timedelta(minutes=1)
    metadata['Injection_marker'] = markerint

    # summary_metadata['File name'] = filepath.split("\\")[-1]
    summary_metadata = {}
    summary_metadata['all metadata'] = metadata
    summary_metadata['Acquisition date'] = acquisition_date
    summary_metadata['Acquisition time'] = acquisition_time
    summary_metadata['Time of application'] = metadata['Injection_marker']

    return summary_metadata


@st.cache_data
def rawdata(filepath):

    # Importing raw data

    first_rawdata = pd.read_csv(filepath, delimiter='\t', skiprows=[0, 1, 2, 3, 4, 5, 6, 8, 9, 10])
    rawdata = first_rawdata.copy()
    rawdata = rawdata.drop(['Unnamed: 0'], axis=1)
    rawdata['Time[min]'] = rawdata['No.'] / 1000 * (1 / 60)
    rawdata.rename(columns={'No.': 'Time[ms]'}, inplace=True)
    list_of_wells = list(rawdata)[1:-1]

    rawdata_dict = {"rawdata": rawdata, "wells": list_of_wells}

    return rawdata_dict

@st.cache_data
def all_plotting(rawdata,threshold):
    with st.spinner('Plotting your data. This might take up to 20 seconds...'):


        from plotly.subplots import make_subplots
        wells = rawdata['wells']
        well = 0

        fig = make_subplots(
            rows=8, cols=12, shared_xaxes=True, vertical_spacing=0.05,
            subplot_titles=wells)

        i, j = 1, 1


        for well in wells:


            fig.add_trace(go.Scatter(x=rawdata['rawdata']['Time[min]'], y=rawdata['rawdata'][well], showlegend=False, name=well,
                                     marker=dict(color='#3366CC')), row=j, col=i)

            x = rawdata['rawdata']['Time[min]']
            y = rawdata['rawdata'][well]

            from scipy.signal import find_peaks

            X = np.array(x.to_numpy())
            Y = np.array(y.to_numpy())

            peaks, properties = find_peaks(Y, prominence=threshold)

            fig.add_trace(go.Scatter(mode='markers', x=x[peaks], y=Y[peaks], showlegend=False,
                                     marker=dict(size=5, color='#EF553B', symbol='triangle-down')), row=j, col=i)

            i += 1
            if i == 13:
                i = 1
                j += 1


        fig.update_layout(height=800, width=1400)

        st.plotly_chart(fig)



    return fig



def well_plot(analysiswell,rawdata,threshold,summary_metadata):

    x = rawdata['rawdata']['Time[min]']
    y = rawdata['rawdata'][analysiswell]

    fig2 = px.line(rawdata['rawdata'], x, y, width=1300, height=700,
                   labels={"Time[min]_int": "Time (minutes)", analysiswell: "Ratio"})
    fig2.update_xaxes(rangeslider_visible=True)

    fig2.add_vline(x=summary_metadata['Time of application'], line_width=3, line_dash="dash", line_color="green")

    from scipy.signal import find_peaks

    X = np.array(x.to_numpy())
    Y = np.array(y.to_numpy())

    peaks, properties = find_peaks(Y, prominence=threshold)

    fig2.add_trace(go.Scatter(mode='markers', x=x[peaks], y=Y[peaks], marker=dict(
        size=10,
        color='#EF553B',
        symbol='triangle-down'
    ), name='Detected Peaks'))

    st.plotly_chart(fig2)

    return fig2


def template(rows,columns):
    # Creating list of letters
    list_letters = []
    start_from = ord('A')
    for i in range(rows):
        list_letters.append(chr(start_from + i))

    # Creating list of numbers
    list_numbers = []
    for i in range(columns):
        list_numbers.append(str(i+1))

    # Creating the dataframe with well names
    dict = {}
    for i in list_numbers:
        temp_list = []
        list_ones = []
        for j in list_letters:
            temp_list.append(j+i)
            list_ones.append(1)
        dict[i] = temp_list

    df = pd.DataFrame(dict)

    return df

