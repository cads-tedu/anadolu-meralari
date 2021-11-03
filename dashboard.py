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
google_years = pd.read_csv('google_years.csv')
google_sites = pd.read_csv('google_sites.csv')
google_title_bigrams = pd.read_csv('google_title_bigrams.csv')
google_content_bigrams = pd.read_csv('google_content_bigrams.csv')

##Sidebar'a başlık ve farklı sayfalar oluşturmak için filtre ekleme
st.sidebar.markdown("# Onarıcı Tarım Ekosisteminin Metinsel Analizi")

sidebar_select = st.sidebar.radio(" ", ('Uygulama Hakkında', 'Tweetler', 'Google Sonuçları'))

if sidebar_select == 'Uygulama Hakkında':
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('## Onarıcı Tarım Ekosisteminin Metinsel Analizi')
        st.markdown(' ')
        st.markdown(' ')
        st.markdown("Bu uygulama, Türkiye'de 'onarıcı tarım' kavramının ve proje paydaşı olan Anadolu Meralarının ekosistemdeki yerini izlemek için geliştirilmiştir. Anadolu Meraları ve alandaki diğer aktörler ile belirlenen bazı kavramlar kullanılarak, Google ve Twitter'dan bu kavramları içeren tweetler ve Google içerikleri veri kazıma yöntemiyle çekilmiştir ve elde edilen verilerin metin madenciliği aracılığıyla analizi gerçekleştirilmiştir.")
        
    with col2:
        st.image('https://www.bugday.org/blog/wp-content/uploads/2020/04/image-asset.jpeg')
       
    st.markdown(' ')
    
    col1, col2, col3 = st.columns([1.4, 0.1, 0.7])
    
    with col1:
        st.markdown("Twitter ve Google arama sonuçlarından veri çekerken kullanılan kavramlar; **'onarıcı tarım', 'bütüncül yönetim', 'permakültür', 'meraların onarımı', 'sürdürülebilir tarım', 'onarım çağı', 'savory enstitüsü', 'bütüncül planlı otlatma', 'agroekoloji', 'yenileyici tarım', 'yeşil gübreleme', 'canlandırıcı tarım', 'fukuoka doğal tarım yöntemi', 'dönüşümlü ekim', 'sürmesiz tarım', 'ekolojik onarım', 'toprağa karbon gömme', 'monokültür tarım', 'doğa temelli çözümler', 'pestisit kullanımı', 'planlı otlatma', 'konvansiyonel hayvancılık', 'dönüm hattı tasarımı', 'pozitif tarım', 'toprak işlemesiz tarım', 'yoğun otlatma', 'iyi tarım uygulamaları', 'doğa dostu tarım', 'iklim dostu tarım', 'insan dostu tarım', 'toprağın su tutma kapasitesi', 'topraktaki organik madde miktarı'**")
 
    with col3:
        st.image('data:image/png;base64,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')
        
if sidebar_select == 'Tweetler':

    st.markdown('## Tweetlerin Metinsel Analizi')
    st.markdown(' ')
    st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen kavramlar kullanılarak Twitter'dan çekilmiştir.")
    
    twitter_keywords = list(twitter.keyword.unique())
    twitter_years = list(twitter.year.unique())
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        keyword_select = st.multiselect('Kavram seçiniz.', twitter_keywords, default = ['sürdürülebilir tarım', 'permakültür', 'pozitif tarım', 'bütüncül yönetim', 'onarıcı tarım'])
        
    with col2:
        year_select = st.multiselect('Yıl seçiniz.', twitter_years, default = twitter_years)
        
    st.markdown(' ')
        
    #Yıllara Göre Tweet Sayısı    
    filtered_years = years[(years.year.isin(year_select)) & (years.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_years = filtered_years.groupby('year')['count'].sum().to_frame().reset_index()
    
    st.markdown('## Yıllara Göre Kavramların Twitter Aramalarındaki Sıklığı')
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Tweet Sayısı", "keyword":"Kavram"})
        fig.update_layout(font=dict(size=15), width=700, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #Tweet Atan Kişiler
    filtered_names = names[(names.year.isin(year_select)) & (names.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_names = filtered_names.name.value_counts().reset_index().rename(columns = {'index':'name', 'name':'count'})
    
    st.markdown('## Kimler bu kavramları içeren tweet atıyor?')
    
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
        
    #Tweetlerdeki İkili Kelimeler
    filtered_tweet_bigrams = tweet_bigrams[(tweet_bigrams.year.isin(year_select)) & (tweet_bigrams.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_tweet_bigrams = filtered_tweet_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    st.markdown('## Twitter Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri')
    
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_tweet_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "Kelime İkilisi","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
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
        google_keyword_select = st.multiselect('Kavram seçiniz.', google_keywords, default = ['sürdürülebilir tarım', 'permakültür', 'pozitif tarım', 'bütüncül yönetim', 'onarıcı tarım'])
        
    with col2:
        google_year_select = st.multiselect('Yıl seçiniz.', google_year, default = google_year)
        
    st.markdown(' ')
        
    #Yıllara Göre Haber Sayısı    
    filtered_years = google_years[(google_years.year.isin(google_year_select)) & (google_years.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_years = filtered_years.groupby('year')['count'].sum().to_frame().reset_index()
    
    st.markdown('## Yıllara Göre Kavramların Google Aramalarındaki Sıklığı')
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Haber Sayısı", "keyword":"Kavram"})
        fig.update_layout(font=dict(size=15), width=700, height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    #Siteler        
    st.markdown('## Google Sonuçlarına Göre En Çok İçerik Üreten Web Siteleri')
     
    filtered_sites = google_sites[(google_sites.year.isin(google_year_select)) & (google_sites.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_sites = filtered_sites.site.value_counts().to_frame().rename(columns = {'site':'count'}).reset_index().rename(columns = {'index':'site'})
   
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_sites.iloc[0:20, :], x = 'count', y = 'site',
                     labels={"site": "Web Sitesi", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig)
        
    #Başlıklarda Kelime Sıklıkları
    st.markdown('## Google Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri - Başlıklar İçin')
    
    filtered_google_title_bigrams = google_title_bigrams[(google_title_bigrams.year.isin(google_year_select)) & (google_title_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_bigrams = filtered_google_title_bigrams.title_bigrams.value_counts().to_frame().rename(columns = {'title_bigrams':'count'}).reset_index().rename(columns = {'index':'title_bigram'})
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.bar(ordered_google_title_bigrams.iloc[0:20, :], x = 'count', y = 'title_bigram',
                     labels={"title_bigram": "Kelime İkilisi","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #İçeriklerde Kelime Sıklıkları
    st.markdown('## Google Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri - İçerikler İçin')
   
    filtered_google_content_bigrams = google_content_bigrams[(google_content_bigrams.year.isin(google_year_select)) & (google_content_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_bigrams = filtered_google_content_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.bar(ordered_google_content_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "Kelime İkilisi","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #Topic Modelling
    #st.header('Topic Modelling')
    
    #col1, col2, col3 = st.columns([0.02, 0.93, 0.05])
    
    #with col2:
        #HtmlFile = open("google_lda4.html", 'r', encoding='utf-8')
        #source_code = HtmlFile.read() 
        #print(source_code)
        #components.html(source_code, height = 800, width = 1250)

    
  




