import nltk
import re
import pickle

if __name__ == "__main__":
    # three lists of tuples being declared
    word_features =[]
    word_pos_features = []
    word_pos_liwc_features = []

    # open files and extract data
    # open and extract word_features
    fword_feat = open( 'word_features-training-features.txt' )
    for lines in fword_feat:

        print(  lines.split(" ",1)[0] ) # gets first word ie positive or negative
    fword_feat.close()
    '''
    # open and extract word_pos_features
    fword_pos_feat = open( 'word_pos_features-training-features.txt' )
    # opena and extract word_pos_liwc_features
    fword_pos_liwc_features = open( 'word_pos_features-training-features.txt' )
    '''
