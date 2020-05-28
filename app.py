import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
from datetime import date
from datetime import timedelta 
import plotly.express as px
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import nltk
import os

# import math
# import datetime
# import re
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# from nltk.probability import FreqDist
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from textblob import textblob
import time
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}], requests_pathname_prefix='/app1/'
)
app.title = "Data Analytics for Brand Improvement"

server = app.server

ls = os.listdir()
while True:
    if "temp.csv" in ls:
        break
    else:
        print("In loop")
        time.sleep(1)
data = pd.read_csv('file.csv',index_col=False)

df = pd.DataFrame(data)

tweets_no = df.shape[0]
retweets_no = 2000
positive_sentiment = df['Sentiments'].value_counts()[1]
last_update_no = date.today() - timedelta(days=1)

### Preprocessing of Text

def preprocess_texts(text):
    stop_words = stopwords.words('english') 
    punc = text.translate(str.maketrans('','', string.punctuation))
    tokens = word_tokenize(punc)
    words = [w for w in tokens if not w in stop_words]
    preprocessed_text = TreebankWordDetokenizer().detokenize(words)
    return preprocessed_text

#### Word CLoud Generation
def plotly_wordcloud(text):
    wc = WordCloud(stopwords = set(STOPWORDS),
                   max_words = 80,
                   max_font_size =100)
    wc.generate(text)
    
    word_list=[]
    freq_list=[]
    fontsize_list=[]
    position_list=[]
    orientation_list=[]
    color_list=[]

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)
        
    # get the positions
    x=[]
    y=[]
    for i in position_list:
        x.append(i[0])
        y.append(i[1])
            
    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i*100)
    new_freq_list
    
    trace = go.Scatter(x=x, 
                       y=y, 
                       textfont = dict(size=new_freq_list,
                                       color=color_list),
                       hoverinfo='text',
                       hovertext=['{0}{1}'.format(w, f) for w, f in zip(word_list, freq_list)],
                       mode='text',  
                       text=word_list
                      )
    
    layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                        'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False}})
    
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig, word_list, freq_list

positive_text = df['text'].loc[df['Sentiments'] == 1].str.cat(sep = ' ')
#negative_text = df['text'].loc[df['Sentiments'] == -1].str.cat(sep = ' ')
negative_text = df['text'].loc[df['Sentiments'] == 0].str.cat(sep = ' ')

positive_text = preprocess_texts(positive_text)
negative_text = preprocess_texts(negative_text)
#neutral_text = preprocess_texts(neutral_text)

fig_pos, pos_text, pos_freq = plotly_wordcloud(positive_text)
fig_neg, neg_text, neg_freq = plotly_wordcloud(negative_text)
#fig_neu, neu_text, neu_freq = plotly_wordcloud(neutral_text)

############################################################################################################
## APPLICATION LAYOUT


app.layout = html.Div(
    [
        # dcc.Store(id="aggregate_data"),
        # # empty Div to trigger javascript file for graph resizing
        # html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("data_analytics.png"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "8px",
                            },
                        )
                    ],
                    className="two columns",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(tweets_no), html.P(html.B("No. of Tweets"))],
                                    id="tweets",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(retweets_no), html.P(html.B("No. of Retweets"))],
                                    id="retweets",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(positive_sentiment), html.P(html.B("No. of Positive sentiments"))],
                                    id="sentiments",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(last_update_no), html.P(html.B("Last Updated"))],
                                    id="last_update",
                                    className="mini_container",
                                ),
                            ],
                            className="row flex-display"
                        )
                    ],
                    className="twelve columns",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                    html.H6("WordCloud for Positive Sentiments"),
                    dcc.Graph(
                        figure = fig_pos
                        )
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
                html.Div(
                    [
                    dcc.Graph(
                            figure={
                                'data': [
                                    {'x': pos_text[:10], 'y': pos_freq[:10], 'type': 'bar', 'orientation': 'v'},
                                ],
                                'layout': {
                                'title': 'Word Frequency Bar chart',
                                'xaxis': {'title': 'Frequency'},
                                'yaxis': {'title': 'Words'}
                                }
                            },
                        )
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
            ],
            className="row container-display",
            style={
                # "margin-left":"-60px",
                "width": "100%"
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                    html.H6("WordCloud for Negative Sentiments"),
                    dcc.Graph(
                        figure = fig_neg
                        )
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
                html.Div(
                    [
                    dcc.Graph(
                            figure={
                                'data': [
                                    {'x': neg_text[:10], 'y': neg_freq[:10], 'type': 'bar', 'orientation': 'v'},
                                ],
                                'layout': {
                                'title': 'Word Frequency Bar chart',
                                'xaxis': {'title': 'Frequency'},
                                'yaxis': {'title': 'Words'}
                                }
                            },
                        )
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
            ],
            className="row container-display",
            style={
                # "margin-left":"-60px",
                "width": "100%"
            }
        ),
        html.Div(
            [
                html.Div(
                    [
                    dcc.Graph(figure = px.histogram(df,x='Subjectivity',title='Histogram on Subjectivity of Sentiments',nbins=20, ))
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
                html.Div(
                    [
                    dcc.Graph(
                            figure = px.histogram(df,x='Sentiments',title='Histogram of frequency distribution Sentiments', )
                        )
                    ],
                    className="pretty_container three columns",
                    style={
                        "width": "inherit",
                    }
                ),
            ],
            className="row container-display",
            style={
                # "margin-left":"-60px",
                "width": "100%"
            }
        )
    ]
)
if __name__=='__main__':
    app.run_server(debug=True)

