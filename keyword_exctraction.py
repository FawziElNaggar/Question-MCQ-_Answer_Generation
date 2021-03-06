# -*- coding: utf-8 -*-
"""KeyWord Exctraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1htZUBZRGo8NEXADD_sh99RuF0rMYuKke
"""

import nltk
import string
import pke
from nltk.corpus import stopwords
import collections
from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor

def Keyword_Extraction(text):
  # 1. create a TfIdf extractor.
  extractor = pke.unsupervised.TfIdf()
  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  # 3. select {1-3}-grams not containing punctuation marks as candidates.
  extractor.candidate_selection(n=3, stoplist=list(string.punctuation))
  # 4. weight the candidates using a `tf` x `idf`
  extractor.candidate_weighting()

  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_TFIDF = extractor.get_n_best(n=10)
  ###############################################################
    # 1. create a KPMiner extractor.
  extractor = pke.unsupervised.KPMiner()

  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  lasf = 5
  cutoff = 200
  extractor.candidate_selection(lasf=lasf, cutoff=cutoff)
  # 4. weight the candidates using KPMiner weighting function.
  alpha = 2.3
  sigma = 3.0
  extractor.candidate_weighting(alpha=alpha, sigma=sigma)
  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_KPMiner = extractor.get_n_best(n=10)
  ###########################################################
    # 1. create a YAKE extractor.
  extractor = pke.unsupervised.YAKE()
  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  stoplist = stopwords.words('english')
  extractor.candidate_selection(n=3, stoplist=stoplist)
  window = 2
  use_stems = False # use stems instead of words for weighting
  extractor.candidate_weighting(window=window,
                                stoplist=stoplist,
                                use_stems=use_stems)
  threshold = 0.8
  keyphrases_Yake = extractor.get_n_best(n=10, threshold=threshold)
  ################################################################
    # TextRank
  
  pos = {'NOUN', 'PROPN', 'ADJ'}
  # 1. create a TextRank extractor.
  extractor = pke.unsupervised.TextRank()

  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  extractor.candidate_weighting(window=2,
                                pos=pos,
                                top_percent=0.33)
  keyphrases_TextRank = extractor.get_n_best(n=10)

  pos = {'NOUN', 'PROPN', 'ADJ'}
  ##############################################################
  # 1. create a SingleRank extractor.
  extractor = pke.unsupervised.SingleRank()
  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)

  # 3. select the longest sequences of nouns and adjectives as candidates.
  extractor.candidate_selection(pos=pos)
  extractor.candidate_weighting(window=10,
                                pos=pos)

  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_SingleRank = extractor.get_n_best(n=10)
  ##############################################################
  # 1. create TopicRank
  extractor = pke.unsupervised.TopicRank()
  # 2. load the content of the document.
  extractor.load_document(input=text)

  # 3. select the longest sequences of nouns and adjectives, that do
  #    not contain punctuation marks or stopwords as candidates.
  pos = {'NOUN', 'PROPN', 'ADJ'}
  stoplist = list(string.punctuation)
  stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
  stoplist += stopwords.words('english')
  extractor.candidate_selection(pos=pos, stoplist=stoplist)
  extractor.candidate_weighting(threshold=0.74, method='average')

  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_TopicRank = extractor.get_n_best(n=10)
  ######################################################################
    # define the valid Part-of-Speeches to occur in the graph
  pos = {'NOUN', 'PROPN', 'ADJ'}

  # define the grammar for selecting the keyphrase candidates
  grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"
  # 1. create a TopicalPageRank extractor.
  extractor = pke.unsupervised.TopicalPageRank()

  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  # 3. select the noun phrases as keyphrase candidates.
  extractor.candidate_selection(grammar=grammar)

  # 4. weight the keyphrase candidates using Single Topical PageRank.
  extractor.candidate_weighting(window=10,pos=pos)

  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_TopicalPageRank = extractor.get_n_best(n=10)
  ############################################################################
  # define the valid Part-of-Speeches to occur in the graph
  pos = {'NOUN', 'PROPN', 'ADJ'}
  # define the grammar for selecting the keyphrase candidates
  grammar = "NP: {<ADJ>*<NOUN|PROPN>+}"
  # 1. create a PositionRank extractor.
  extractor = pke.unsupervised.PositionRank()
  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)
  # 3. select the noun phrases up to 3 words as keyphrase candidates.
  extractor.candidate_selection(grammar=grammar,
                                maximum_word_number=3)
  # 4. weight the candidates using the sum of their word's scores that are
  extractor.candidate_weighting(window=10,
                                pos=pos)
  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_PositionRank = extractor.get_n_best(n=10)
  #################################################################
    # 1. create a MultipartiteRank extractor.
  extractor = pke.unsupervised.MultipartiteRank()
  # 2. load the content of the document.
  extractor.load_document(input=text)
  # 3. select the longest sequences of nouns and adjectives, that do
  #    not contain punctuation marks or stopwords as candidates.
  pos = {'NOUN', 'PROPN', 'ADJ'}
  stoplist = list(string.punctuation)
  stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
  stoplist += stopwords.words('english')
  extractor.candidate_selection(pos=pos, stoplist=stoplist)
  # 4. build the Multipartite graph and rank candidates using random walk,
  extractor.candidate_weighting(alpha=1.1,
                                threshold=0.74,
                                method='average')
  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_MultipartiteRank = extractor.get_n_best(n=10)
  ####################################################################
    # define a list of stopwords
  stoplist = stopwords.words('english')
  # 1. create a Kea extractor.
  extractor = pke.supervised.Kea()

  # 2. load the content of the document.
  extractor.load_document(input=text,
                          language='en',
                          normalization=None)

  # 3. select 1-3 grams that do not start or end with a stopword as
  #    candidates. Candidates that contain punctuation marks as words
  #    are discarded.
  extractor.candidate_selection(stoplist=stoplist)
  extractor.candidate_weighting()
  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_Kea = extractor.get_n_best(n=10)
  #######################################################################

    # 1. create a WINGNUS extractor.
  extractor = pke.supervised.WINGNUS()
  # 2. load the content of the document.
  extractor.load_document(input=text)
  # 3. select simplex noun phrases as candidates.
  extractor.candidate_selection()
  extractor.candidate_weighting()
  # 5. get the 10-highest scored candidates as keyphrases
  keyphrases_WINGNUS = extractor.get_n_best(n=10)
  ########################################################################
  ## Concate All Keywords
  Keywords= keyphrases_TFIDF + keyphrases_KPMiner + keyphrases_Yake + keyphrases_TextRank +keyphrases_SingleRank + keyphrases_TopicRank + keyphrases_TopicalPageRank +keyphrases_PositionRank + keyphrases_MultipartiteRank + keyphrases_Kea + keyphrases_WINGNUS
  Keywords = [k for k,v in Keywords] 
  ########################################################################
  ## find_Repeted_Keyword
  duplicated_Keywords=[item for item, count in collections.Counter(Keywords).items() if count > 1]  
  return duplicated_Keywords

def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    # Remove any short sentences less than 20 letters.
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences

def get_sentences_for_keyword(Keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in Keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)

    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
        df = pd.DataFrame({'values':values})
        df.drop_duplicates(inplace = True)
        keyword_sentences[key] = df['values'].tolist()

    return keyword_sentences

def keyword_sentenceMapping(text):
  sentences = tokenize_sentences(text)
  duplicated_Keywords = Keyword_Extraction(text)
  keyword_sentence_mapping_after = get_sentences_for_keyword(duplicated_Keywords, sentences)
  keyword_sentence_mapping={key: value for key, value in keyword_sentence_mapping_after.items() if value}
  return keyword_sentence_mapping