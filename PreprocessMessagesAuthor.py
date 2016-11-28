__author__ = 'patrickjameswhite'
import sqlite3
import pandas as pd
import nltk
import os

directory = os.path.dirname(os.path.abspath(__file__))

db_path = '/Users/patrickjameswhite/Library/Messages/chat.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

#copy and pasted text, like summarization text

text_msgs = [str(row[0]).strip() for row in c.execute('SELECT text FROM message WHERE is_from_me == 1')]

#filtering the empties that got through :|
text_msgs = list(filter((lambda x: x != '￼' and x != '￼￼'),text_msgs))

text_msgs_all = ' '.join(text_msgs)


#holds the words and there respective positions within the phrase normalized
word_place_dict = {}
for row in text_msgs:
    row_words = nltk.tokenize.word_tokenize(row)

    enum_row_words = [((num+1)/len(row_words),x) for num,x in enumerate(row_words)]

    for word in enum_row_words:
        #word[0] place in sentence/phrase, word[1] actual tokenized word
        if word[1] in word_place_dict:
            word_place_dict[word[1]].append(word[0])

        else:
            word_place_dict[word[1]] = [word[0]]


for x,y in word_place_dict.items():
    word_place_dict[x] = sorted(y)


#final list that contains the authors word placements, (word,its place in the sentence/phrase
sorted_list_word_place = sorted(map(list, word_place_dict.items()))

#final list that is like above, but puts the values in columns as opposed to having it all in one column
#sorted_list_word_place = [[k]+[x for x in v] for k,v in word_place_dict.items()]
#for x in sorted_list_word_place:
#    print(x)

text_msgs_words = nltk.tokenize.word_tokenize(text_msgs_all)
freq_dist = nltk.FreqDist(text_msgs_words)

freq_dist = freq_dist.most_common(None)

sum_freq = max([x[1] for x in freq_dist])

norm_freq_dist = [(tup[0],float(tup[1])/sum_freq) for tup in freq_dist]

headers_norm_freq_dist = ["word","dist"]
headers_norm_word_place = ["word","norm_place"]


preprocessed_norm_freq_dist = pd.DataFrame(data=norm_freq_dist,columns=headers_norm_freq_dist)

preprocessed_norm_freq_dist.to_csv(path_or_buf=directory+"/Preprocessed/norm_freq_dist.csv",columns=headers_norm_freq_dist)

preprocessed_norm_word_place = pd.DataFrame(data=sorted_list_word_place,columns=headers_norm_word_place)

preprocessed_norm_word_place.to_csv(path_or_buf=directory+"/Preprocessed/word_place.csv",columns=headers_norm_word_place)






