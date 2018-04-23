# nltk-sentiment-analysis
A natural language processing probabilistic model for processing natural languages, namely in sentiment analysis in restaurant reviews.  We train a Naive Bayes classifier to automatically label unseen reviews as positive or negative. 

## feature_vector.py
feature_vector.py is the main program.  
It requires an additional filename be presented in order to process the feature vector for that file.
If a file is not present, the program prompts the user for correct input and then exits.

USAGE: $ feature_vector.py [filename_in_directory_to_be_processed]

feature_vector.py calls data_helper.py for parsing through the data to obtain overall review score and the text
of the review

### note on usage
the call to write files uses splicing.  the command expects
that if you give a filename to feature_vector that is 
not one of the three we were given, you must make sure
it has at least 10 chars before the DATASET name and 5 chars
after.  This is because it splices: restaurant- (10) dataset .data (5).

if You are getting an error with a new file, this may be the case


