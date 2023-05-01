# Importing the dependencies
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import numpy as np
import requests
import pickle
import datetime

import panel as pn
import holoviews as hv
import hvplot.pandas

st.set_page_config(page_title='Audio Analyzer Dashboard', page_icon= '🎧', layout='centered', initial_sidebar_state='collapsed')


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#-- Load assets
lottie_audio_wave = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_vixkj2dq.json")

#-- Header Section
with st.container():
    st.title('Audio Analyzer Dashboard 🎧')
    st.subheader('Transcribe and get new insights into your audio files with AI')
    st_lottie(lottie_audio_wave, key='music wave')
    
#-- Side bar
with st.container():
    #input field to accept audio url
    audio_url = st.sidebar.text_input(label='Insert audio url', value='')
    url = "https://github.com/msherrif04/Audio-Analyzer-Dashboard/blob/master/data/audio.mp3?raw=true"
    st.sidebar.audio(url)
    #c--Implement code to send url to assembly aid and save transcript
    
    #loading the data
    with open(r'notebooks\transcript_response.pkl', 'rb') as f:
        data=pickle.load(f)
    
    buffer = data['text']
    #download button 
    download_transcript_button = st.sidebar.download_button('Download transcript', data= buffer, file_name = 'transcript.txt', mime='str')


# --Sentiment analysis section --# 
# Graph for sentiment analysis
sentiment = data['sentiment_analysis_results']
sentiment_df= pd.DataFrame(sentiment)
sentiment_df_grouped = sentiment_df['sentiment'].value_counts()
sentiment_plot = sentiment_df_grouped.hvplot(title='Sentences by Sentiment Category', kind='bar')

# #--dataframes for each sentiment
positive_df = sentiment_df[sentiment_df["sentiment"] == "POSITIVE"][["text", "sentiment"]]
negative_df = sentiment_df[sentiment_df["sentiment"] == "NEGATIVE"][["text", "sentiment"]]
neutral_df = sentiment_df[sentiment_df["sentiment"] == "NEUTRAL"][["text", "sentiment"]]

with st.container():
    st.header('Sentiment Analysis')

    st.subheader('Sentiment Chart')
    st.bokeh_chart(hv.render(sentiment_plot, backend='bokeh'))
    
    st.write('---')
    
    st.subheader('Sentences with Sentiment')
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
    
#--Auto Chapter Summary Section --#
st.write('---')
class ButtonAudio():
    def __init__(self, starttime):
        self.start_time = starttime
        
        left_col, right_col = st.columns([1,5])
        with left_col:
            self.button = st.button(label=str(datetime.timedelta(0, int(self.start_time/1000))), key= starttime, on_click = self.reset_audio_head,type='primary', use_container_width=True)
        with right_col:
            self.chapter_audio = st.audio(url, start_time= round(self.start_time/1000))
        
        # str(int(self.start_time/1000))
        
    def reset_audio_head(self):
        self.chapter_audio = st.audio(url, start_time= round(self.start_time/1000))

chapters= data['chapters']
highlights = []

for index, chapter in enumerate(chapters):
    with st.container():
        st.header('chapter ' + str(index) + ' Summary')
        st.write(chapter['summary'])
        audio_button = ButtonAudio(chapter['start'])
        st.write('---')

#--Auto Highlights -- #
highlights = data['auto_highlights_result']['results']
highlights_df = pd.DataFrame(highlights)
with st.container():
    st.header('Important words and phrases')
    st.dataframe(highlights_df)