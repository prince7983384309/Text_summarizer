""" This is a text summarizer project in which i am usinig NLP and some libraries named NLTK and SPACY.
    For the front end GUI interface, I am using streamlit. Noe let's start ------
"""
# if there is no NLTK and SPACY packages in the system than intall first.

#####   First I am using NLTK   --------------------------------------------------------------------
# Import libraries for NLTK

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq

# making the function for NLTK 
def nltk_summarizer(text):
    Stop_words = set(stopwords.words("english"))   # using stopwords in english
    words = word_tokenize(text)
    freq_table = dict()                                # frequency dict for the words in text


    for word in words:
        word = word.lower()                        # change the all words into lowercase
        if word not in stopwords:
            if word in freq_table:
                freq_table[word] += 1              # if any word with frequency table it will add else
            else:
                freq_table[word] = 1               # add in frequency table


    sentence_list = sent_tokenize(text)
    max_freqency =  max(freq_table.values())
    for word in freq_table.keys():
        freq_table[word]  = (freq_table[word]/max_freqency)

    sentence_score = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq_table.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = freq_table[word]
                    else:
                        sentence_score[sent] += freq_table[word]

# use heap-based priority queue (heapq)
    summary_sentences = heapq.nlargest(10, sentence_score, key= sentence_score.get)
    summary = " ".join(summary_sentences)
    return summary




##### making the function for SPACY -------------------------------------------------------------- 
# import libraries
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

# making the function for SPACY
def spacy_summarizer(text):
    stop_words = list(STOP_WORDS)
    words = word_tokenize(text)
    freq_table = dict()

    for word in words:
        word = word.lower()                        # change the all words into lowercase
        if word not in stopwords:
            if word in freq_table:
                freq_table[word] += 1              # if any word with frequency table it will add else
            else:
                freq_table[word] = 1               # add in frequency table

    sentence_list = sent_tokenize(text)
    max_freqency =  max(freq_table.values())
    for word in freq_table.keys():
        freq_table[word]  = (freq_table[word]/max_freqency)

    sentence_score = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in freq_table.keys():
                if len(sent.split(" ")) < 30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = freq_table[word]
                    else:
                        sentence_score[sent] += freq_table[word]

    # use heap-based priority queue (heapq)
    summary_sentences = heapq.nlargest(10, sentence_score, key= sentence_score.get)
    summary = " ".join(summary_sentences)
    return summary

#### Now for GUI use streamlit -------------------------------------------------------------------
import streamlit as st
import re

# making function for GUI and text cleaning 
def gui():
    st.title("Text Summarizer")
    activity = ["summarize by given text"]
    choice = st.sidebar.selectbox("select activity", activity)

    if choice == "summarize by given text":
        st.subheader("summary by NLP")
        article_text = st.text_area("enter text here", "type here")

        # now clean the text
        article_text = re.sub(r'\[[0-9]*\]', '', article_text)
        article_text = re.sub('[^a-zA-Z.,]', ' ',article_text)
        article_text = re.sub(r"\b[a-zA-Z]\b",'',article_text)
        article_text = re.sub("[A-Z]\Z",'',article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        summary_choice = st.selectbox("summary choice", ['NLTK', 'SPACY'])
        if st.button("summarize by given text"):
            if summary_choice == 'NLTK':
                summary_result = nltk_summarizer(article_text)
            elif summary_choice == 'SPACY':
                summary_result = spacy_summarizer(article_text)

            st.write(summary_result)

if __name__=='__main__':
    gui()
