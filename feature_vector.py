
import nltk
import re
import json
#import word_category_counter
import data_helper
import argparse

def concatStr(ngram):
    out=""
    for key, value in ngram.items():
        out+= "{}:{} ".format( key, value )
    return out


def fwrite_feature_vectors( posi_word_ngram, neg_word_ngram, posi_pos_ngram, neg_pos_ngram, liwc ):
    '''
    this is some nasty code and I am not the most proud of it
    there does exist a more elegant way to do this but
    I am not the best with python.  This is not very DRY
    although it still gets the job done
    '''
    dataset = 'help' # this shall be the changed variable

    # initialize and open files,
    # This overwrites old files and initializes the category
    '''
    with open( 'word_features-'+dataset+'-features.txt', "w", encoding="utf-8") as fout:
        fout.write('positive ')

    # write positive word_features
    for key, value in posi_word_ngram.items():
        with open( 'word_features-'+dataset+'-features.txt', "a", encoding="utf-8") as fout:
            fout.write( "{}:{} ".format( key, value ) )

    # append negative word_features
    with open( 'word_features-'+dataset+'-features', "a", encoding="utf-8") as fout:
        fout.write('\n') # newline to seperate positive and negative
        fout.write('negative ')
        for key, value in neg_word_ngram.items():
            fout.write( "{}:{} ".format( key, value ) )

    '''

    pos_word_feat=concatStr(posi_word_ngram)
    neg_word_feat=concatStr(neg_word_ngram)

    posi_pos_feat = concatStr( posi_pos_ngram )
    neg_pos_feat  = concatStr( neg_pos_ngram )

    with open( 'word_features-'+dataset+'-features.txt', "w", encoding="utf-8" ) as fout:
        fout.write( "positive %s\nnegative %s"%( pos_word_feat, neg_word_feat ) )

    with open( 'word_pos_features-'+dataset+'features.txt',"w", encoding="utf-8" ) as fout:
        fout.write( "positive %s %s\n negative %s %s"%( pos_word_feat, posi_pos_feat, neg_word_feat, neg_pos_feat ) )

    return


def get_ngram_features(tokens):
    '''
    This function creates the unigram and bigram features as described in
    the assignment3 handout.

    :param tokens:
    :return: feature_vectors: a dictionary values for each ngram feature
    TODO change this
    '''
    feature_vectors = {}
    uni_fdist = nltk.FreqDist(tokens)
    bi_fdist = nltk.FreqDist(nltk.bigrams(tokens))
    for token, freq in uni_fdist.items():
        feature_vectors["UNI_{0}".format(token)] = float(freq)/uni_fdist.B()
    for (b1, b2), freq in bi_fdist.items():
        feature_vectors["BIGRAM_{0}_{1}".format(b1, b2)] = float(freq)/bi_fdist.N()

    return feature_vectors

def get_pos( text ):
    tags = []
    words = []

    words = get_words( text )   # tokenize words
    tags = [ t[1] for t in nltk.pos_tag( words ) ]
    return tags

def get_words( text ):
    '''
    This function performs part of speech tagging and extracts the words
    from the review text.

        - tokenize the text into sentences
        - word tokenize each sentence

    Returns a list containing all the words of the review and another list
    '''
    # tokenization for each sentence
    words = []
    sentences = nltk.sent_tokenize( text )
    for sent in sentences:
        sent = sent.lower()
        words += nltk.word_tokenize( sent )

    #tags=[ t[1] for t in nltk.pos_tag(words) ]

    #print( tags )
    #print( words )
    return words

def features_stub():
    # open restaurant-training.data
    # calls data_helper.py to put file in pos or neg category list
    # here is where I would call other files as well
    datafile = "restaurant-help.data"
    raw_data = data_helper.read_file(datafile)
    positive_texts, negative_texts = data_helper.get_reviews(raw_data)

    # category_texts creates
    #   { posive, [... all positive reviews ] , negative, [...all neg ...] }
    #
    #category_texts = {"positive": positive_texts, "negative": negative_texts}
    #feature_set = "word_features"
    positive_toks = []
    positive_pos_toks = []
    negative_toks = []
    negative_pos_toks = []

    # get word and pos tokens not the most
    # efficient but easier to trace
    for documents in positive_texts:
        positive_toks += get_words( documents )
    for documents in negative_texts:
        negative_toks += get_words( documents )

    for documents in positive_texts:
        positive_pos_toks += get_pos( documents )
    for documents in negative_texts:
        negative_pos_toks += get_pos( documents )

    # get ngrams for positive and negative categories
    posi_word_ngram = {}
    posi_pos_ngram = {}
    neg_word_ngram = {}
    neg_pos_ngram = {}

    for tokens in positive_toks:
        posi_word_ngram.update( get_ngram_features( positive_toks ) )
    for tokens in negative_toks:
        neg_word_ngram.update( get_ngram_features( negative_toks ) )

    for tokens in positive_toks:
        posi_pos_ngram.update( get_ngram_features( positive_pos_toks ) )
    for tokens in negative_toks:
        neg_pos_ngram.update( get_ngram_features( negative_pos_toks ) )

    liwc = 'six'
    fwrite_feature_vectors( posi_word_ngram, neg_word_ngram, posi_pos_ngram, neg_pos_ngram, liwc )

if __name__ == "__main__":
    features_stub()

