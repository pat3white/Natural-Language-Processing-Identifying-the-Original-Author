__author__ = 'patrickjameswhite'

import sqlite3
import pandas as pd
import nltk
import os
import csv
import ast

directory = os.path.dirname(os.path.abspath(__file__))

db_path = '/Users/patrickjameswhite/Library/Messages/chat.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

#copy and pasted text, like summarization text

text_msgs_me = [[row[0],1,0,0] for row in c.execute('SELECT text FROM message WHERE is_from_me == 1')]
text_msgs_haters = [[row[0],0,0,0] for row in c.execute('SELECT text FROM message WHERE is_from_me == 0')]
text_msgs_all = text_msgs_me + text_msgs_haters
#print(len(text_msgs_all))
#for x,y in text_msgs_all[:10]:
#    print(x,y)



norm_freq_dist_pd = pd.read_csv(directory+"/Preprocessed/norm_freq_dist.csv")
word_place_pd = pd.read_csv(directory+"/Preprocessed/word_place.csv")

freq_dist = {}
word_place = {}

for x in norm_freq_dist_pd.iterrows():
    word = x[1][1]
    freq = x[1][2]
    freq_dist[word] = freq

for x in word_place_pd.iterrows():
    word = x[1][1]
    places = x[1][2]
    word_place[word] = ast.literal_eval(places)


def distance(lista, point):

    return sum((point- a) ** 2 for a in lista) ** .5

for x in text_msgs_all:
    #print(x)
    try:
        words = nltk.tokenize.word_tokenize(x[0])
    except TypeError:
        words = []

    def conv_to_freq(word,freq_dist):
        try:
            return freq_dist[word]
        except KeyError:
            return 0

    try:
        freq_score = sum([conv_to_freq(word,freq_dist) for word in words]) / len(words)
    except ZeroDivisionError:
        #word/phrase is None, disregard
        continue

    enum_row_words = [((num+1)/len(words),w) for num,w in enumerate(words)]

    def fetch_value(word,word_place):
        try:
            return word_place[word]
        except KeyError:
            return [-1]
    try:
        word_place_score = sum([distance(fetch_value(p[1],word_place),p[0]) for p in enum_row_words]) / len(words)
    except ZeroDivisionError:
        #word/phrase is None, disregard
        continue

    x[2] = freq_score
    x[3] = word_place_score

sum_freq = max([x[2] for x in text_msgs_all])
sum_places = max([x[3] for x in text_msgs_all])

norm_text_msgs_all = [(tup[0],tup[1],float(tup[2])/sum_freq,1 - float(tup[3])/sum_places) for tup in text_msgs_all]

headers_norm_text_msgs_all = ['sentence','if_me','freq_score','struc_score']
preprocessed_norm_word_place = pd.DataFrame(data=norm_text_msgs_all,columns=headers_norm_text_msgs_all)

preprocessed_norm_word_place.to_csv(path_or_buf=directory+"/Preprocessed/preprocessed.csv",columns=headers_norm_text_msgs_all)






