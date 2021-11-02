# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 09:30:19 2021

@author: cansu
"""
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import streamlit.components.v1 as components

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")

## Sayfayı genişletme
def _max_width_():
    max_width_str = f"max-width: 4000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
    
_max_width_()


##Veriyi yükleme
twitter = pd.read_csv('twitter.csv')
google = pd.read_csv('google_results.csv')
years = pd.read_csv('tweet_years.csv') 
names = pd.read_csv('tweet_names.csv') 
hashtags = pd.read_csv('hashtags.csv')
mentions = pd.read_csv('mentions.csv')
tweet_bigrams = pd.read_csv('tweet_bigrams.csv') 
tweet_words = pd.read_csv('tweet_words.csv')
google_years = pd.read_csv('google_years.csv')
google_sites = pd.read_csv('google_sites.csv')
google_title_words = pd.read_csv('google_title_words.csv')
google_title_bigrams = pd.read_csv('google_title_bigrams.csv')
google_content_words = pd.read_csv('google_content_words.csv')
google_content_bigrams = pd.read_csv('google_content_bigrams.csv')

##Sidebar'a başlık ve farklı sayfalar oluşturmak için filtre ekleme
st.sidebar.markdown("# Onarıcı Tarım Ekosisteminin Metinsel Analizi")

sidebar_select = st.sidebar.radio(" ", ('Tweetler', 'Google Sonuçları'))

if sidebar_select == 'Tweetler':

    st.title('Tweetlerin Metinsel Analizi')
    st.markdown(' ')
    st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen kavramlar kullanılarak Twitter'dan çekilmiştir.")
    
    twitter_keywords = list(twitter.keyword.unique())
    twitter_years = list(twitter.year.unique())
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        keyword_select = st.multiselect('Kavram seçiniz.', twitter_keywords, default = twitter_keywords)
        
    with col2:
        year_select = st.multiselect('Yıl seçiniz.', twitter_years, default = twitter_years)
        
    st.markdown(' ')
        
    #Yıllara Göre Tweet Sayısı    
    filtered_years = years[(years.year.isin(year_select)) & (years.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_years = filtered_years.groupby('year')['count'].sum().to_frame().reset_index()
    
    col1, col2, col3 = st.columns([1, 1.5, 0.1])
    
    with col1:
        st.markdown('## Yıla Göre Tweet Sayıları')
        fig = px.line(ordered_years, x = 'year', y = 'count',
                     labels={"year": "Yıl", "count": "Tweet Sayısı"})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('## Yıla ve Kavrama Göre Tweet Sayıları')
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Tweet Sayısı", "keyword":"Kavram"})
        st.plotly_chart(fig, use_container_width=True)
        
    #Tweet Atan Kişiler
    filtered_names = names[(names.year.isin(year_select)) & (names.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_names = filtered_names.name.value_counts().reset_index().rename(columns = {'index':'name', 'name':'count'})
    
    st.markdown('## Bu kavramları içeren tweet atan kişiler kimler?')
    
    col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
    
    with col2:
        wordcloud = WordCloud(background_color="black", max_words=len(ordered_names))
        d = {}
        for i in range(len(ordered_names)):
            d[ordered_names['name'][i]] = ordered_names['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[15,5])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    st.header('Tweetlerdeki Hashtagler ve Mentionlar')
    
    filtered_hashtags = hashtags[(hashtags.year.isin(year_select)) & (hashtags.keyword.isin(keyword_select))].reset_index(drop = True)
    orderes_hashtags = filtered_hashtags.hashtag.value_counts().reset_index().rename(columns = {'index':'hashtag', 'hashtag':'count'})
    filtered_mentions = mentions[(mentions.year.isin(year_select)) & (mentions.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_mentions = filtered_mentions.mention.value_counts().reset_index().rename(columns = {'index':'mention', 'mention':'count'})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('### Hashtagler')
        wordcloud = WordCloud(background_color="black", max_words=len(orderes_hashtags))
        d = {}
        for i in range(len(orderes_hashtags)):
            d[orderes_hashtags['hashtag'][i]] = orderes_hashtags['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[15,5])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    with col2:
        st.markdown('### Mentionlar')
        wordcloud = WordCloud(background_color="black", max_words=len(ordered_mentions))
        d = {}
        for i in range(len(ordered_mentions)):
            d[ordered_mentions['mention'][i]] = ordered_mentions['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[15,5])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    #Tweetlerdeki Kelimeler
    filtered_tweet_words = tweet_words[(tweet_words.year.isin(year_select)) & (tweet_words.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_tweet_words = filtered_tweet_words.words.value_counts().to_frame().rename(columns = {'words':'count'}).reset_index().rename(columns = {'index':'word'})
    
    st.markdown('## Tweetlerde En Sık Kullanılan Kelimeler')
    
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_tweet_words.iloc[0:20, :], x = 'count', y = 'word',
                     labels={"word": "Kelime", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig)
        
    #Tweetlerdeki İkili Kelimeler
    filtered_tweet_bigrams = tweet_bigrams[(tweet_bigrams.year.isin(year_select)) & (tweet_bigrams.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_tweet_bigrams = filtered_tweet_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    st.markdown('## Tweetlerde En Sık Kullanılan İkili Kelimeler')
    
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_tweet_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig)

    #st.header('Topic Modelling')
    
    #col1, col2, col3 = st.columns([0.02, 0.93, 0.05])
    
    #with col2:
        #HtmlFile = open("tweets_lda5.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #print(source_code)
        #components.html(source_code, height = 800, width = 1250)
        
    
if sidebar_select == 'Google Sonuçları':

    st.title('Google Sonuçlarının Metinsel Analizi')
    st.markdown(' ')
    st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen kavramlar kullanılarak Google'dan çekilmiştir.")
    
    google_keywords = list(google.keyword.unique())
    google_year = list(google.year.unique())
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        google_keyword_select = st.multiselect('Kavram seçiniz.', google_keywords, default = google_keywords)
        
    with col2:
        google_year_select = st.multiselect('Yıl seçiniz.', google_year, default = google_year)
        
    st.markdown(' ')
        
    #Yıllara Göre Haber Sayısı    
    filtered_years = google_years[(google_years.year.isin(google_year_select)) & (google_years.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_years = filtered_years.groupby('year')['count'].sum().to_frame().reset_index()
    
    col1, col2, col3 = st.columns([1, 1.5, 0.1])
    
    with col1:
        st.markdown('## Yıla Göre Haber Sayıları')
        fig = px.line(ordered_years, x = 'year', y = 'count',
                     labels={"year": "Yıl", "count": "Haber Sayısı"})
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown('## Yıla ve Kavrama Göre Haber Sayıları')
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Haber Sayısı", "keyword":"Kavram"})
        st.plotly_chart(fig, use_container_width=True)
    
    #Siteler        
    st.markdown('## En Çok İçerik Üreten Haber Siteleri')
     
    filtered_sites = google_sites[(google_sites.year.isin(google_year_select)) & (google_sites.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_sites = filtered_sites.site.value_counts().to_frame().rename(columns = {'site':'count'}).reset_index().rename(columns = {'index':'site'})
   
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_sites.iloc[0:20, :], x = 'count', y = 'site',
                     labels={"site": "Web Sitesi", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig)
        
    #Başlıklarda Kelime Sıklıkları
    st.markdown('## Google Sonuçları Başlıklarında En Sık Kullanılan Kelimeler')
    
    filtered_google_title_words = google_title_words[(google_title_words.year.isin(google_year_select)) & (google_title_words.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_words = filtered_google_title_words.title_words.value_counts().to_frame().rename(columns = {'title_words':'count'}).reset_index().rename(columns = {'index':'title_word'})
    
    filtered_google_title_bigrams = google_title_bigrams[(google_title_bigrams.year.isin(google_year_select)) & (google_title_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_bigrams = filtered_google_title_bigrams.title_bigrams.value_counts().to_frame().rename(columns = {'title_bigrams':'count'}).reset_index().rename(columns = {'index':'title_bigram'})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = px.bar(ordered_google_title_words.iloc[0:20, :], x = 'count', y = 'title_word',
                     labels={"title_word": "Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.bar(ordered_google_title_bigrams.iloc[0:20, :], x = 'count', y = 'title_bigram',
                     labels={"title_bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #İçeriklerde Kelime Sıklıkları
    st.markdown('## Google Sonuçları İçeriklerinde En Sık Kullanılan Kelimeler')
    
    filtered_google_content_words = google_content_words[(google_content_words.year.isin(google_year_select)) & (google_content_words.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_words = filtered_google_content_words.words.value_counts().to_frame().rename(columns = {'words':'count'}).reset_index().rename(columns = {'index':'word'})
    
    filtered_google_content_bigrams = google_content_bigrams[(google_content_bigrams.year.isin(google_year_select)) & (google_content_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_bigrams = filtered_google_content_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = px.bar(ordered_google_content_words.iloc[0:20, :], x = 'count', y = 'word',
                     labels={"word": "Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.bar(ordered_google_content_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_layout(width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #Topic Modelling
    #st.header('Topic Modelling')
    
    #col1, col2, col3 = st.columns([0.02, 0.93, 0.05])
    
    #with col2:
        #HtmlFile = open("google_lda4.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #print(source_code)
        #components.html(source_code, height = 800, width = 1250)

    
  




