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
import plotly.graph_objects as go

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
st.sidebar.title("Onarıcı Tarım Ekosisteminin Metinsel Analizi")

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
    
    col1, col2, col3 = st.columns([1.3, 0.25, 0.6])
    
    with col1:
        st.markdown("Twitter ve Google arama sonuçlarından veri çekerken kullanılan kavramlar; **'onarıcı tarım', 'bütüncül yönetim', 'permakültür', 'meraların onarımı', 'sürdürülebilir tarım', 'onarım çağı', 'savory enstitüsü', 'bütüncül planlı otlatma', 'agroekoloji', 'yenileyici tarım', 'yeşil gübreleme', 'canlandırıcı tarım', 'fukuoka doğal tarım yöntemi', 'dönüşümlü ekim', 'sürmesiz tarım', 'ekolojik onarım', 'toprağa karbon gömme', 'monokültür tarım', 'doğa temelli çözümler', 'pestisit kullanımı', 'planlı otlatma', 'konvansiyonel hayvancılık', 'dönüm hattı tasarımı', 'pozitif tarım', 'toprak işlemesiz tarım', 'yoğun otlatma', 'iyi tarım uygulamaları', 'doğa dostu tarım', 'iklim dostu tarım', 'insan dostu tarım', 'toprağın su tutma kapasitesi', 'topraktaki organik madde miktarı'**")
 
if sidebar_select == 'Tweetler':
    
    st.markdown('## Tweetlerin Metinsel Analizi')
    st.markdown(' ')
    
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen 32 kavram kullanılarak Twitter'dan çekilmiştir. Veri seti, kavramları içeren bu zamana kadar atılmış 19522 tweeti ve bu tweetleri atan kullanıcıların isimlerini içermektedir. Aşağıdaki filtrelerden incelemek istediğiniz kavramları ve yılları seçtiğinizde, bu kavramları içeren tüm tweetlerin analizlerine ulaşabilirsiniz. Sayfanın devamında oluşturulan bütün grafikler aşağıdaki kavram ve yıl seçiminize göre güncellenmektedir.")
    
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
    
    st.markdown('### Yıllara Göre Kavramların Tweetlerdeki Kullanım Sıklığı')
    st.markdown(' ')
    st.markdown('Aşağıdaki grafik, seçtiğiniz kavramların seçtiğiniz yıllar içinde kaç tweet içinde geçtiğini göstermektedir.')
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Tweet Sayısı", "keyword":"Kavram"})
        fig.update_layout(font=dict(size=15), width=700, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #Tweet Atan Kişiler
    filtered_names = names[(names.year.isin(year_select)) & (names.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_names = filtered_names.name.value_counts().reset_index().rename(columns = {'index':'name', 'name':'count'})
    
    st.markdown('### Kimler bu kavramları içeren tweet atıyor?')
    st.markdown(' ')
    
    col1, col2 = st.columns([1.6, 1])
    
    with col1:
        st.markdown("Aşağıdaki wordcloud, seçtiğiniz kavramları kullanarak tweet atan kişi ve kurumların isimlerini göstermektedir. Kullanıcının diğer kullanıcılara göre bu kavramları içeren ne kadar çok tweeti varsa ismi o kadar büyük gözükmektedir.")
    
    st.markdown(' ')
    
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
    
    st.markdown(' ')
    st.markdown('### Tweetlerdeki Hashtagler ve Mentionlar')
    
    filtered_hashtags = hashtags[(hashtags.year.isin(year_select)) & (hashtags.keyword.isin(keyword_select))].reset_index(drop = True)
    orderes_hashtags = filtered_hashtags.hashtag.value_counts().reset_index().rename(columns = {'index':'hashtag', 'hashtag':'count'})
    filtered_mentions = mentions[(mentions.year.isin(year_select)) & (mentions.keyword.isin(keyword_select))].reset_index(drop = True)
    ordered_mentions = filtered_mentions.mention.value_counts().reset_index().rename(columns = {'index':'mention', 'mention':'count'})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('### Hashtagler')
        st.markdown("Aşağıdaki wordcloud, seçtiğiniz kavramları içeren tweetlerde en çok kullanılan hashtagleri göstermektedir.")
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
        st.markdown("Aşağıdaki wordcloud, seçtiğiniz kavramları içeren tweetlerde mentionla bahsedilen ekosistem aktörlerini göstermektedir. Bu kişi ve kurumların bazıları ikincil aktörler olarak yorumlanabilir.")
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
    ordered_tweet_bigrams = ordered_tweet_bigrams[~ordered_tweet_bigrams.bigram.isin(keyword_select)]
    
    st.markdown(' ')
    st.markdown('### Twitter Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri')
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown('Aşağıdaki grafik, seçtiğiniz kavramları içeren tweetlerde en sık bir arada kullanılan kelime ikililerini göstermektedir.')
    
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_tweet_bigrams.iloc[0:20, :], x = 'count', y = 'bigram',
                     labels={"bigram": "Kelime İkilisi","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig)

    #Tweet Tablosu    
    st.markdown('## Tweetler')
    st.markdown(' ')
    st.markdown('Seçtiğiniz yıllarda atılmış, seçtiğiniz kavramları içeren tweetleri aşağıdaki tabloda görebilirsiniz.')
    
    filtered_tweets = twitter[(twitter.keyword.isin(keyword_select)) & (twitter.year.isin(year_select))][['datetime', 'username', 'name', 'text', 'year', 'keyword']].rename(columns = {'datetime':'Tarih-Saat', 'username':'Kullanıcı Adı', 'name':'İsim', 'text':'Tweet'})
    
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        table_year = st.multiselect('Yıl seçiniz.', list(filtered_tweets.year.unique()), default = list(filtered_tweets.year.unique()))
        
    with col2:
        table_name = st.text_input('İsim giriniz.', list(filtered_tweets.İsim.unique()))
     
    with col3:
        table_keyword = st.multiselect('Kavram seçiniz.', list(filtered_tweets.keyword.unique()), default = list(filtered_tweets.keyword.unique()))
        
    filtered_tweets = filtered_tweets[(filtered_tweets.year.isin(table_year)) & (filtered_tweets.keyword.isin(table_keyword)) & (filtered_tweets.İsim == table_name)]
        
    fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4],
        columnwidth = [200,200,200,600],
        header=dict(values=list(['Tarih-Saat', 'Kullanıcı Adı', 'İsim', 'Tweet']),
                    fill_color= '#f63366', font=dict(color='white'), align='center'),
        cells=dict(values=[filtered_tweets['Tarih-Saat'], filtered_tweets['Kullanıcı Adı'], filtered_tweets['İsim'], filtered_tweets['Tweet']],
                   fill_color='#f0f2f6', align='center'))])
        
    fig.update_layout(margin=dict(l=20, r=0, b=0, t=0))
    fig.update_layout(width=1200)
    st.plotly_chart(fig)
        
    
if sidebar_select == 'Google Sonuçları':

    st.markdown('## Google Sonuçlarının Metinsel Analizi')
    st.markdown(' ')
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("Bu uygulamada kullanılan veri seti, alanla ilgili belirlenen 32 kavram kullanılarak Google arama sonuçlarından çekilmiştir. Veri seti, belirlenen kavramlarla yapılan Google aramalarında 2014 yılından itibaren çıkan web sitelerinin içeriklerinden oluşmaktadır. Veri seti, 6100 web sitesi içeriğine sahiptir. Aşağıdaki filtrelerden incelemek istediğiniz kavramları ve yılları seçtiğinizde, bu kavramları içeren web sitesi içeriklerine ulaşabilirsiniz. Sayfanın devamında oluşturulan bütün grafikler aşağıdaki kavram ve yıl seçiminize göre güncellenmektedir.")
    
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
    
    st.markdown('### Yıllara Göre Kavramların Google Aramalarındaki Sıklığı')
    st.markdown(' ')
    st.markdown('Aşağıdaki grafik, seçtiğiniz kavramların seçtiğiniz yıllar içinde kaç web sitesi içeriğinde geçtiğini göstermektedir.')
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.line(filtered_years, x = 'year', y = 'count', color = 'keyword',
                     labels={"year": "Yıl", "count": "Haber Sayısı", "keyword":"Kavram"})
        fig.update_layout(font=dict(size=15), width=700, height=600)
        st.plotly_chart(fig, use_container_width=True)
    
    #Siteler        
    st.markdown('### Google Sonuçlarına Göre En Çok İçerik Üreten Web Siteleri')
    st.markdown(' ')
    st.markdown('Aşağıdaki grafik, seçtiğiniz kavramları kullanarak en çok içerik üreten web sitelerini göstermektedir.')
     
    filtered_sites = google_sites[(google_sites.year.isin(google_year_select)) & (google_sites.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_sites = filtered_sites.site.value_counts().to_frame().rename(columns = {'site':'count'}).reset_index().rename(columns = {'index':'site'})
   
    col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
    
    with col2:
        fig = px.bar(ordered_sites.iloc[0:20, :], x = 'count', y = 'site',
                     labels={"site": "Web Sitesi", "count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig)
        
    #Başlıklarda Kelime Sıklıkları
    st.markdown('### Google Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri - Başlıklar İçin')
    st.markdown(' ')
    st.markdown('Aşağıdaki grafik, seçtiğiniz kavramları içeren web sitesi başlıklarında en sık bir arada kullanılan kelime ikililerini göstermektedir.')
    
    filtered_google_title_bigrams = google_title_bigrams[(google_title_bigrams.year.isin(google_year_select)) & (google_title_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_title_bigrams = filtered_google_title_bigrams.title_bigrams.value_counts().to_frame().rename(columns = {'title_bigrams':'count'}).reset_index().rename(columns = {'index':'title_bigram'})
    ordered_google_title_bigrams = ordered_google_title_bigrams[~ordered_google_title_bigrams.title_bigram.isin(google_keyword_select)]
    
    col1, col2, col3 = st.columns([0.05, 0.85, 0.1])
        
    with col2:
        fig = px.bar(ordered_google_title_bigrams.iloc[0:20, :], x = 'count', y = 'title_bigram',
                     labels={"title_bigram": "Kelime İkilisi","count": "Sıklık"})
        fig.update_layout(yaxis=dict(autorange="reversed"), font=dict(size=15), width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
    #İçeriklerde Kelime Sıklıkları
    st.markdown('### Google Sonuçlarına Göre En Sık Bir Arada Kullanılan Kelime İkilileri - İçerikler İçin')
    st.markdown(' ')
    st.markdown('Aşağıdaki grafik, seçtiğiniz kavramları içeren web sitesi içeriklerinde en sık bir arada kullanılan kelime ikililerini göstermektedir.')
   
    filtered_google_content_bigrams = google_content_bigrams[(google_content_bigrams.year.isin(google_year_select)) & (google_content_bigrams.keyword.isin(google_keyword_select))].reset_index(drop = True)
    ordered_google_content_bigrams = filtered_google_content_bigrams.bigrams.value_counts().to_frame().rename(columns = {'bigrams':'count'}).reset_index().rename(columns = {'index':'bigram'})
    ordered_google_content_bigrams = ordered_google_content_bigrams[~ordered_google_content_bigrams.bigram.isin(google_keyword_select)]
    
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

    
  




