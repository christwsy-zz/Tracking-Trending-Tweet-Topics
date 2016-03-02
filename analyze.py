# STEPS
# 1. tokenize
# 2. remove stopwords
# 3. lemma
# 4. find synonym set, calculate the similarity

import json
import nltk
from collections import Counter
from prettytable import PrettyTable
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize

noun_tags = ["NN", "NNS", "NNP", "NNPS"]

def extractNouns(tweets):
    nouns = []
    for tweet in tweets:
        tagged = nltk.pos_tag(word_tokenize(tweet))
        nouns = [word for word, pos in tagged if pos in noun_tags]
        nouns.append(' '.join(nouns))
    return nouns

def removeStopword(tweets):
    stopwords = sw.words('english')
    temp = []
    for tweet in tweets:
        querywords = tweet.split()
        resultwords  = [word for word in querywords if word.lower() not in stopwords]
        result = ' '.join(resultwords)
        print result
        temp.append(result)
    return temp

def preprosessing(data):
    raise NotImplementedError

def run():
    filename = '../data/201602260343.json'
    file = open(filename)
    status_texts = []

    i = 0
    maximum_item = 5 # the maximum number of items to store
    
    for line in file:
        if i < maximum_item:
            if 'delete' not in line:
                status_texts.append(json.loads(line)['text'])
                i = i + 1
            else:
                continue
        else:
            break
    # test
    status_texts = removeStopword(status_texts)
    print status_texts
    print '\n\n'
    print extractNouns(status_texts)
    words = word_tokenize(status_texts[2])
    print nltk.pos_tag(words)


run()


# ###### TESTING
# status_texts = [ status['text'] for status in statuses ]
# screen_names = [ user_mention['screen_name'] for status in statuses
#                 for user_mention in status['entities']['user_mentions'] ]
# hashtags = [ hashtag['text'] for status in statuses
#                 for hashtag in status['entities']['hashtags'] ]

# print wn.synsets('computer')
# print wn.synset('computer.n.01').lemma_names()


