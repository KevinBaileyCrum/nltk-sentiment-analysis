import sys
import nltk
import re
import json
import word_category_counter
import data_helper
import argparse

def concat_str(ngram):
    # helper function for fwrite_feature_vectors

    out=""
    for key, value in ngram.items():
        out+= "{}:{} ".format( key, value )
    return out


def fwrite_feature_vectors( filename, posi_word_ngram, neg_word_ngram, posi_pos_ngram, neg_pos_ngram, posi_liwc_feat, neg_liwc_feat ):
    '''
    writes out to files
    if using a new file other than trainning, development, or testing,
    make sure the output is correct for the parsing of dataset to filename
    '''
    dataset = filename[11:-5]

    # Formats output to be written as string formats
    # format word tokens
    pos_word_feat=concat_str(posi_word_ngram)
    neg_word_feat=concat_str(neg_word_ngram)
    # format pos_tokens
    posi_pos_feat = concat_str( posi_pos_ngram )
    neg_pos_feat  = concat_str( neg_pos_ngram )
    # format LIWC tokens
    posi_liwc_feat = concat_str( posi_liwc_feat )
    neg_liwc_feat  = concat_str( neg_liwc_feat )

    # write to files
    with open( 'word_features-'+dataset+'-features.txt', "w", encoding="utf-8" ) as fout:
        fout.write( "positive %s\nnegative %s"%( pos_word_feat, neg_word_feat ) )

    with open( 'word_pos_features-'+dataset+'-features.txt',"w", encoding="utf-8" ) as fout:
        fout.write( "positive %s %s\n negative %s %s"%( pos_word_feat, posi_pos_feat, neg_word_feat, neg_pos_feat ) )

    with open( 'word_pos_liwc_features-'+dataset+'-features.txt',"w", encoding="utf-8" ) as fout:
        fout.write( "positive %s %s %s\n negative %s %s %s"%( pos_word_feat, posi_pos_feat, posi_liwc_feat,neg_word_feat, neg_pos_feat, neg_liwc_feat ) )
    return


def get_liwc_features(words):
    """
    Adds a simple LIWC derived feature
    :param words:
    :return:
    """
    feature_vectors = {}
    text = " ".join(words)
    liwc_scores = word_category_counter.score_text(text)

    # All possible keys to the scores start on line 269
    # of the word_category_counter.py script

    negative_score = 0
    positive_score = 0

    # some values were too high so scalars are present
    negative_score += liwc_scores["Negative Emotion"] * 2
    negative_score += liwc_scores["Anger"]
    negative_score += liwc_scores["Anxiety"]
    negative_score += liwc_scores["Sadness"]
    negative_score += liwc_scores["Metaphysical issues"]
    negative_score += liwc_scores["Death"]

    positive_score += liwc_scores["Positive Emotion"] / 6
    positive_score += liwc_scores["Optimism and energy"]
    positive_score += liwc_scores["Achievement"]
    positive_score += liwc_scores["Future Tense"]


    if positive_score > negative_score:
        feature_vectors["liwc:positive"] = 1
    else:
        feature_vectors["liwc:negative"] = 1

    return feature_vectors


def get_ngram_features(tokens):
    '''
    This function creates the unigram and bigram features as described in
    the assignment3 handout.

    :param tokens:
    :return: feature_vectors: a dictionary values for each ngram feature
    '''
    # TODO change this
    feature_vectors = {}
    uni_fdist = nltk.FreqDist(tokens)
    bi_fdist = nltk.FreqDist(nltk.bigrams(tokens))
    for token, freq in uni_fdist.items():
        feature_vectors["UNI_{0}".format(token)] = float(freq)/uni_fdist.N()
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

    regex = re.compile(r'(?:\w)+')
    normalized_words = []
    for w in words:
        normalized_words += ( re.findall( regex, w ) )

    #tags=[ t[1] for t in nltk.pos_tag(words) ]

    #print( tags )
    #print( words )
    return normalized_words

def features_stub( filename ):
    # open restaurant-training.data
    # calls data_helper.py to put file in pos or neg category list
    # here is where I would call other files as well
    datafile = filename
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
    print( 'begin tokenize')
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
    print( 'tokenizing compl' )
    # get ngrams for positive and negative categories
    posi_word_ngram = {}
    posi_pos_ngram = {}
    neg_word_ngram = {}
    neg_pos_ngram = {}
    print( 'begin word ngram' )
    for tokens in positive_toks:
        posi_word_ngram.update( get_ngram_features( tokens ) )
    print( 'all positive word ngram completed')
    print( 'begin negative word ngram' )
    for tokens in negative_toks:
        neg_word_ngram.update( get_ngram_features( tokens ) )
    print( 'all negative word ngram completed')
    print( 'end word ngram' )

    print( 'begin pos ngram' )
    for tokens in positive_toks:
        posi_pos_ngram.update( get_ngram_features( tokens ) )

    print( 'all pos pos ngram completed')
    print( 'begin negative ngram' )
    for tokens in negative_toks:
        neg_pos_ngram.update( get_ngram_features( tokens ) )
    print( 'all negative pos ngram completed')
    print( 'end pos ngram')
    print('begin liwc')
    # get LIWC features
    posi_liwc_feat = get_liwc_features( positive_toks )
    neg_liwc_feat  = get_liwc_features( negative_toks )
    print('end liwc')
    print('begin file write')
    fwrite_feature_vectors( filename, posi_word_ngram, neg_word_ngram, posi_pos_ngram, neg_pos_ngram, posi_liwc_feat, neg_liwc_feat )

if __name__ == "__main__":
    if( len( sys.argv ) < 2 ):
        print( "error: feature_vector.py called with too few args")
        print( "usage: python feature_vector.py [single_file_to_process]" )
        print( "note: you also want LIWC files set up as in project description")
        exit()

    print( "%s processing"%( sys.argv[1]) )
    filename = sys.argv[1]
    features_stub( filename )
    print( "completed" )
