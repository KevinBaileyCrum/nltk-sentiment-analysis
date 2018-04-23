import nltk
import re
import pickle

if __name__ == "__main__":
    # three lists of tuples being declared
    word_features = []
    word_tuple =()
    word_pos_features = []
    word_pos_liwc_features = []

    # open files and extract data
    # open and extract word_features
    with open( 'word_features-training-features.txt', 'r' ) as f:
        for line in f:
            word_features.append( line.split() )
            #for word in line.split():
            #    word_features.append( word )

    word_features[0].pop(0) # remove positive
    word_features[1].pop(0) # remove negative
    word_tuple += word_features[0], 'positive'
    word_tuple += word_features[1], 'negative'
    #print( word_features[0] )
    #print( word_features[1] )
    print( word_tuple )

    classifier = nltk.classify.NaiveBayesClassifier.train( word_tuple )
    '''
    # open and extract word_pos_features
    fword_pos_feat = open( 'word_pos_features-training-features.txt' )
    # opena and extract word_pos_liwc_features
    fword_pos_liwc_features = open( 'word_pos_features-training-features.txt' )
    '''
