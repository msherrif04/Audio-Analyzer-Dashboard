# -- Importing depencies-- #
import streamlit as st
import pandas as pd
import numpy as np
import panel as pn
import hvplot.pandas
import pickle
import io
from io import StringIO

import holoviews as hv

# --Loading the data--#
with open(r'notebooks\transcript_response.pkl','rb') as f:
    data = pickle.load(f)
    
#--Download the transcript --#
# buffer = StringIO()
# buffer.write(data["text"])
# buffer.seek(0)
# buffer
buffer = data['text']
type(buffer)

#Class for audio button function

def reset_audio_head():
    pass

# --Components--#
# Graph for sentiment analysis
sentiment = data['sentiment_analysis_results']
sentiment_df= pd.DataFrame(sentiment)
sentiment_df_grouped = sentiment_df['sentiment'].value_counts()
sentiment_plot = sentiment_df_grouped.hvplot(title='Sentences by Sentiment Category', kind='bar')

#--dataframes for each sentiment
positive_df = sentiment_df[sentiment_df["sentiment"] == "POSITIVE"][["text", "sentiment"]]
negative_df = sentiment_df[sentiment_df["sentiment"] == "NEGATIVE"][["text", "sentiment"]]
neutral_df = sentiment_df[sentiment_df["sentiment"] == "NEUTRAL"][["text", "sentiment"]]

#--Audio playback --#
url = "https://github.com/msherrif04/Audio-Analyzer-Dashboard/blob/master/data/audio.mp3?raw=true"
# audio_file = open(url, 'rb')
# audio_bytes = audio_file.read()

#-- Auto chapter summary
chapters= data['chapters']


#--streamlit dashboard layout--#
st.write('hello world')
audio_url = st.text_input(label='Audio url', value='')
st.download_button('Download Transcript', data = buffer, file_name='transcript.txt', mime='str')

st.audio(url) #full audio file 

# audio head for each chapter
for chapter in chapters:
    start_time = int(chapter['start']/1000)
    st.header(chapter['gist'])
    col1, col2, col3 = st.columns([0.5,2,3], gap='small')
    button = col1.button(label=str(start_time))
    audio = col2.audio(url, start_time= start_time)
    summary= col3.write(chapter['summary'])

st.bokeh_chart(hv.render(sentiment_plot, backend='bokeh'))

tab1, tab2, tab3 = st.tabs(['Positive', 'Negative', 'Neutral'])
with tab1:
    st.header('Positive Sentiments')
    st.dataframe(positive_df)

with tab2:
    st.header('Negative Sentiments')
    st.dataframe(negative_df)
    
with tab3:
    st.header('Neutral Sentiments')
    st.dataframe(neutral_df)
    

