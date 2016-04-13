# STEPS
# 1. tokenize 
# 2. remove stopwords
# 3. lemma
# 4. find synonym set, calculate the similarity

import gensim
import json
import networkx as nx
import nltk
import pandas as pd
import re
from collections import defaultdict
from gensim import corpora, models, similarities
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize

noun_tags = ["NN", "NNS", "NNP", "NNPS"]
stemmer = SnowballStemmer("english")
stopwords = sw.words('english')
not_words = ["https", "http"] # manually added blacklist word list

# Extract all nouns from tweets
def extractNouns(tweet):
    nouns = []
    tagged = nltk.pos_tag(word_tokenize(tweet)) # find pos tags for each word
    propernouns = [word for word, pos in tagged if pos in noun_tags and word not in not_words]
    return ' '.join(propernouns)

# Remove all the stopwords and those are not actual words from the tweets
def cleanTweet(tweet):
    resultwords = [word.lower() for word in tweet.split() 
                    if word.lower() not in stopwords and wn.synsets(word)] # removes non-word
    resultwords = [stemmer.stem(word) for word in resultwords]
    if resultwords != []: 
        return ' '.join(resultwords)
    return ''
    
# Find all distinct synonyms of all words in a tweet
def findSynonyms(tweet):
    result = []
    for word in word_tokenize(tweet):
        result.append(word)
        for synset in wn.synsets(word):
            for lemma in synset.lemmas():
                result.append(lemma.name().lower())
    return set(result)
    
def preprosessing(data):
    raise NotImplementedError

def run():
    filename = '../data/201603010120.json' # local data file
    file = open(filename)

    frequency = defaultdict(int)
    status_texts = []
    i = 0
    maximum_item = 10000 # the maximum number of items to store
    
    for line in file:
        if i < maximum_item:
            temp = json.loads(line)
            
            # ignore tweets that have the "delete" key
            # "delete" key indicates that the tweet is deleted
            if "delete" not in temp:
                # if i == 0: first_time = temp["created_at"]
                # print temp["text"]
                cleaned = cleanTweet(extractNouns(temp["text"]))
                if cleaned != '':
                    status_texts.append(cleaned)
                    i += 1
            else:
                continue
                
                
        # When i reach the threshold (which is maximum_item)
        else:
            for text in status_texts:
                for token in text.split():
                    frequency[token] += 1
            
            status_texts = [[token for token in text.split() if frequency[token] > 1] 
                            for text in status_texts]
            
            # print status_texts
            dictionary = corpora.Dictionary(status_texts)
            # dictionary.save('/tmp/deerwester.dict') # save dictionary to file
            # print dictionary            
            # print(dictionary.token2id)
            
            new_doc = "I am watching this new movie called The Carrier. Gross!!"
            new_doc = cleanTweet(new_doc)
            new_vec = dictionary.doc2bow(new_doc.lower().split())
            # print new_vec
            
            corpus = [dictionary.doc2bow(text) for text in status_texts]
            # corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
            # print corpus

            lda = models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=20)
            # print lda
            # print lda[new_vec]
            print lda.print_topics(num_topics=10, num_words=5)
            i = 0
            status_texts = []
            break
            
    # dictionary = corpora.Dictionary(status_texts)
    # corpus = [dictionary.doc2bow(text) for text in status_texts]
    
run()
