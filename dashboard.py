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
hashtags = pd.read_csv('hashtags.csv')
mentions = pd.read_csv('mentions.csv')
tweet_bigrams = pd.read_csv('tweet_bigrams.csv') 
tweet_words = pd.read_csv('tweet_words.csv')
sites = pd.read_csv('sites.csv')
google_title_words = pd.read_csv('google_title_words.csv')
google_title_bigrams = pd.read_csv('google_title_bigrams.csv')
google_content_words = pd.read_csv('google_content_words.csv')
google_content_bigrams = pd.read_csv('google_content_bigrams.csv')

##Sidebar'a başlık ve farklı sayfalar oluşturmak için filtre ekleme
st.sidebar.markdown("# Onarıcı Tarım Ekosisteminin Metinsel Analizi")

sidebar_select = st.sidebar.radio(" ", ('Tweetler', 'Google Sonuçları'))

if sidebar_select == 'Tweetler':

    #Tweet Atan Kişiler
    names = twitter.groupby(['year', 'keyword'])['name'].value_counts().to_frame().rename(columns = {'name':'count'}).reset_index()

    st.title('Tweetlerin Metinsel Analizi')
    st.markdown(' ')
    st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen kavramlar kullanılarak Twitter'dan çekilmiştir.")
    
    row0_1, row0_2 = st.beta_columns((1, 1))
    
    with row0_1:
        keyword_select = st.multiselect('Kavram seçiniz.', list(twitter.keyword.unique()), default = list(twitter.keyword.unique()))
        
    with row0_2:
        year_select = st.multiselect('Yıl seçiniz.', list(twitter.year.unique()), default = list(twitter.year.unique()))
        
    filtered_names = names[(names.year.isin(year_select)) & (names.keyword.isin(keyword_select))].reset_index(drop = True)
    
    st.header('Bu kavramları içeren tweet atan kişiler kimler?')
    
    row1_1, row1_2, row1_3 = st.beta_columns((0.1, 0.7, 0.2))
    
    with row1_2:
        wordcloud = WordCloud(background_color="black", max_words=names.name.nunique())
        d = {}
        for i in range(len(filtered_names)):
            d[filtered_names['name'][i]] = filtered_names['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[10, 5])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    st.header('Tweetlerdeki Hashtagler ve Mentionlar')
    
    filtered_hashtags = hashtags[(hashtags.year.isin(year_select)) & (hashtags.keyword.isin(keyword_select))].reset_index(drop = True)
    filtered_mentions = mentions[(mentions.year.isin(year_select)) & (mentions.keyword.isin(keyword_select))].reset_index(drop = True)
    
    row2_1, row2_2 = st.beta_columns((1, 1))
    
    with row2_1:
        st.markdown('Hashtagler')
        wordcloud = WordCloud(background_color="black", max_words=hashtags.hashtag.nunique())
        d = {}
        for i in range(len(filtered_hashtags)):
            d[filtered_hashtags['hashtag'][i]] = filtered_hashtags['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[10, 8])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    with row2_2:
        st.markdown('Mentionlar')
        wordcloud = WordCloud(background_color="black", max_words=mentions.mention.nunique())
        d = {}
        for i in range(len(filtered_mentions)):
            d[filtered_mentions['mention'][i]] = filtered_mentions['count'][i]
        wordcloud.generate_from_frequencies(d)
        plt.figure(figsize=[10, 8])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
        
    st.header('Tweetlerde En Sık Kullanılan Kelimeler')
    
    filtered_tweet_words = tweet_words[(tweet_words.year.isin(year_select)) & (tweet_words.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_tweet_words = filtered_tweet_words.words.value_counts().to_frame().rename(columns = {'words':'count'}).reset_index().rename(columns = {'index':'word'})
    
    row3_1, row3_2, row3_3 = st.beta_columns((0.1, 0.7, 0.2))
    
    with row3_2:
        fig = px.bar(ordered_tweet_words.iloc[0:20, :], x = 'count', y = 'word',
                     labels={"word": "Kelime", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    st.header('Tweetlerde En Sık Kullanılan İkili Kelimeler')
    
    filtered_tweet_bigrams = tweet_bigrams[(tweet_bigrams.year.isin(year_select)) & (tweet_bigrams.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_tweet_bigrams = filtered_tweet_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    row4_1, row4_2, row4_3 = st.beta_columns((0.1, 0.7, 0.2))
    
    with row4_2:
        fig = px.bar(ordered_tweet_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)

    st.header('Topic Modelling')
    
    row5_1, row5_2, row5_3 = st.beta_columns((0.02, 0.93, 0.05))
    
    with row5_2:
        HtmlFile = open("tweets_lda5.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        print(source_code)
        components.html(source_code, height = 800, width = 1250)
        
    
if sidebar_select == 'Google Sonuçları':

    st.title('Google Sonuçlarının Metinsel Analizi')
    st.markdown(' ')
    st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen kavramlar kullanılarak Google'dan çekilmiştir.")
    
    row0_1, row0_2 = st.beta_columns((1, 1))
    
    with row0_1:
        google_keyword_select = st.multiselect('Kavram seçiniz.', list(google_content_words.keyword.unique()), default = list(google_content_words.keyword.unique()))
        
    with row0_2:
        google_year_select = st.multiselect('Yıl seçiniz.', list(google_content_words.year.unique()), default = list(google_content_words.year.unique()))
        
    #Haber Sayısı
    
    st.header('Yıllara Göre Haber Sayısı')
    
    filtered_year = google[google.keyword.isin(google_keyword_select)].reset_index(drop = True)
    ordered_year = filtered_year.groupby('year').size().to_frame().reset_index().rename(columns = {0:'count'})
    
    row1_1, row1_2, row1_3 = st.beta_columns((0.1, 0.7, 0.2))
    
    with row1_2:
        fig = px.bar(ordered_year, x="year", y="count",
                     labels={"year": "Yıl", "count": "Haber Sayısı"})
        st.plotly_chart(fig)
    
    #Siteler        
    st.header('En Çok İçerik Üreten Haber Siteleri')
     
    filtered_sites = sites[(sites.year.isin(google_year_select)) & (sites.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_sites = filtered_sites.site.value_counts().to_frame().rename(columns = {'site':'count'}).reset_index().rename(columns = {'index':'site'})
   
    row2_1, row2_2, row2_3 = st.beta_columns((0.1, 0.7, 0.2))
    
    with row2_2:
        fig = px.bar(ordered_sites.iloc[0:20, :], x = 'count', y = 'site',
                     labels={"site": "Web Sitesi", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    #Başlıklarda Kelime Sıklıkları
    st.header('Google Sonuçları Başlıklarında En Sık Kullanılan Kelimeler')
    
    filtered_google_title_words = google_title_words[(google_title_words.year.isin(google_year_select)) & (google_title_words.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_words = filtered_google_title_words.title_words.value_counts().to_frame().rename(columns = {'title_words':'count'}).reset_index().rename(columns = {'index':'title_word'})
    
    filtered_google_title_bigrams = google_title_bigrams[(google_title_bigrams.year.isin(google_year_select)) & (google_title_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_bigrams = filtered_google_title_bigrams.title_bigrams.value_counts().to_frame().rename(columns = {'title_bigrams':'count'}).reset_index().rename(columns = {'index':'title_bigram'})
    
    row3_1, row3_2 = st.beta_columns((1, 1))
    
    with row3_1:
        fig = px.bar(ordered_google_title_words.iloc[0:20, :], x = 'count', y = 'title_word',
                     labels={"title_word": "Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    with row3_2:
        fig = px.bar(ordered_google_title_bigrams.iloc[0:20, :], x = 'count', y = 'title_bigram',
                     labels={"title_bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    #İçeriklerde Kelime Sıklıkları
    st.header('Google Sonuçları İçeriklerinde En Sık Kullanılan Kelimeler')
    
    filtered_google_content_words = google_content_words[(google_content_words.year.isin(google_year_select)) & (google_content_words.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_words = filtered_google_content_words.words.value_counts().to_frame().rename(columns = {'words':'count'}).reset_index().rename(columns = {'index':'word'})
    
    filtered_google_content_bigrams = google_content_bigrams[(google_content_bigrams.year.isin(google_year_select)) & (google_content_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_bigrams = filtered_google_content_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    row4_1, row4_2 = st.beta_columns((1, 1))
    
    with row4_1:
        fig = px.bar(ordered_google_content_words.iloc[0:20, :], x = 'count', y = 'word',
                     labels={"word": "Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    with row4_2:
        fig = px.bar(ordered_google_content_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "İkili Kelime","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig)
        
    #Topic Modelling
    st.header('Topic Modelling')
    
    row5_1, row5_2, row5_3 = st.beta_columns((0.02, 0.93, 0.05))
    
    with row5_2:
        HtmlFile = open("google_lda4.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        print(source_code)
        components.html(source_code, height = 800, width = 1250)

    
  




