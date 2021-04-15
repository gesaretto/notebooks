#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Functions useful for SeinfeldBot

## Currently using this lemmatizer to extract only nouns. Let's see how that goes.
### Problem is, much of the speech in Seinfeld is heavy on verbs and idioms. Do we really want to exclude all of that?
### Maybe we should start with all the parts in place, and then eliminate everything but the nouns to see how that works.

import re
import spacy
import random
from scipy.spatial.distance import cosine 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

english_stopwords = stopwords.words("english") + ["n't", "Ca"]
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_md")

# Note: the lemmatizer keeps only nouns, to allow for faster processing and to find more relevant answers.
# Can be tweaked by swapping the commented lines.

def lemmatize_with_pos(sentence):
    # tag_dict = {"N": "n"}
    tag_dict = {"J": "a", "R": "r", "V": "v", "N": "n"}
    lemmatized_sentence = []
    tokenized_sentence = word_tokenize(sentence)
    for token, tag in pos_tag(tokenized_sentence):
        if lemmatizer.lemmatize(tag[0].upper()) in tag_dict:
            lemmatized = lemmatizer.lemmatize(token, tag_dict[tag[0].upper()])
            lemmatized_sentence.append(lemmatized)
    return lemmatized_sentence

# else:
#    lemmatized = lemmatizer.lemmatize(token)
        

def preprocess_sentence(sentence):
    word_regex = "\w+"
    preprocessed_sentence = [lemma for lemma in lemmatize_with_pos(sentence) if re.match(word_regex, lemma) and lemma not in english_stopwords]
    return preprocessed_sentence

def bow_sentence(preprocessed_sentence):
    sentence_bow = {lemma for lemma in preprocessed_sentence}
    return sentence_bow

# This function would find the closest term in the character's BOW based on the Spacy word embeddings for English.
# It's very slow, though; so it's currently not in use. 

def find_closest_in_bow(term, bow, utterances_list):
    term_vector = nlp(term).vector
    lowest_score = 1.0
    closest_word = ""
    for word in bow:
        word_vector = nlp(word).vector
        current_cosine = cosine(term_vector, word_vector)
        # print("...still thinking...")
        # print(current_cosine)
        if current_cosine < lowest_score:
            print("**mumble mumble**", random.choice(utterances_list), "**mumble**")
            lowest_score = current_cosine
            closest_word = word
    return closest_word

def compare_bows(bow_1, bow_2):
    bag_of_matches = {term for term in bow_1 if term in bow_2}
    return (len(bag_of_matches), bag_of_matches)

