
import nltk
import re
import json
#import word_category_counter
import data_helper



def normalize(token, should_normalize=True):
    """
    This function performs text normalization.

    If should_normalize is False then we return the original token unchanged.
    Otherwise, we return a normalized version of the token, or None.

    For some tokens (like stopwords) we might not want to keep the token. In
    this case we return None.

    :param token: str: the word to normalize
    :param should_normalize: bool
    :return: None or str
    """
    if not should_normalize:
        normalized_token = token

    else:

        ###     YOUR CODE GOES HERE
        print('hello')
    return normalized_token



def get_words_tags(text, should_normalize=True):
    """
    This function performs part of speech tagging and extracts the words
    from the review text.

    need to :
        - tokenize the text into sentences
        - word tokenize each sentence
        - part of speech tag the words of each sentence

    Returns a list containing all the words of the review and another list
    containing all the part-of-speech tags for those words.

    :param text:
    :param should_normalize:
    :return:
    """
    words = []
    tags = []

    # tokenization for each sentence

    sent = nltk.sent_tokenize( text )
    for sentences in sent:
        sentences = sentences.lower()
        words += nltk.word_tokenize( sentences )

    tags=[ t[1] for t in nltk.pos_tag(words) ]

    print( tags )
    print( words )
    print()
    print('######################################')

    return words, tags


def get_ngram_features(tokens):
    """
    This function creates the unigram and bigram features as described in
    the assignment3 handout.

    :param tokens:
    :return: feature_vectors: a dictionary values for each ngram feature
    """
    feature_vectors = {}


    ###     YOUR CODE GOES HERE
    raise NotImplemented

    return feature_vectors


def get_pos_features(tags):
    """
    This function creates the unigram and bigram part-of-speech features
    as described in the assignment3 handout.

    :param tags: list of POS tags
    :return: feature_vectors: a dictionary values for each ngram-pos feature
    """
    feature_vectors = {}

    ###     YOUR CODE GOES HERE
    raise NotImplemented

    return feature_vectors


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
    negative_score = liwc_scores["Negative Emotion"]
    positive_score = liwc_scores["Positive Emotion"]
    feature_vectors["Negative Emotion"] = negative_score
    feature_vectors["Positive Emotion"] = positive_score

    if positive_score > negative_score:
        feature_vectors["liwc:positive"] = 1
    else:
        feature_vectors["liwc:negative"] = 1

    return feature_vectors


FEATURE_SETS = {"word_pos_features", "word_features", "word_pos_liwc_features"}

def get_features_category_tuples(category_text_dict, feature_set):
    """

    You will might want to update the code here for the competition part.

    :param category_text_dict:
    :param feature_set:
    :return:
    """
    features_category_tuples = []
    texts = []

    assert feature_set in FEATURE_SETS, "unrecognized feature set:{}, Accepted values:{}".format(feature_set, FEATURE_SETS)

    for category in category_text_dict:
        for text in category_text_dict[category]:

            words, tags = get_words_tags(text)
            feature_vectors = {}

            ###     YOUR CODE GOES HERE

            print( feature_vectors )
            features_category_tuples.append((feature_vectors, category))
            texts.append(text)

    return features_category_tuples, texts


def write_features_category(features_category_tuples, outfile_name):
    """
    Save the feature values to file.

    :param features_category_tuples:
    :param outfile_name:
    :return:
    """
    with open(outfile_name, "w", encoding="utf-8") as fout:
        for (features, category) in features_category_tuples:
            fout.write("{0:<10s}\t{1}\n".format(category, features))


def features_stub():
    # open restaurant-training.data
    # calls data_helper.py to put file in pos or neg category list
    datafile = "restaurant-training.data"
    raw_data = data_helper.read_file(datafile)
    positive_texts, negative_texts = data_helper.get_reviews(raw_data)

    # category_texts creates
    #   { posive, [... all positive reviews ] , negative, [...all neg ...] }
    #
    category_texts = {"positive": positive_texts, "negative": negative_texts}
    feature_set = "word_features"

    features_category_tuples, texts = get_features_category_tuples(category_texts, feature_set)

    #raise NotImplemented
    #filename = "???"
    #write_features_category(features_category_tuples, filename)



if __name__ == "__main__":
    features_stub()

