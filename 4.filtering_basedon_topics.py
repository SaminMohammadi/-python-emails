import argparse
import os
import numpy as np
import csv
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()



# To run
'''
python 4.filtering_basedon_topics.py [--folder_name 'folder'] [--topics ''] [--usecase_keywords ''] [--output_related_topics '']
'''



##################################
#########Input Arguments##########
##################################
def parse_args():
    parser = argparse.ArgumentParser(description="Run 6.filtering_basedon_topics.py")

    parser.add_argument('--folder_name', nargs='?', default='folder', help='input/output folder')
    parser.add_argument('--topics', nargs='?', default='output_topics.txt', help='Input topics corpus')

    parser.add_argument('--usecase_keywords', nargs='?', default='keywords_lemmatized.txt', help='Input keywords corpus')

        ####################
    parser.add_argument('--output_related_topics', nargs='?', default='related_topics_emails.txt', help='related topics file')
        ####################
    return parser.parse_args()





args = parse_args()
folder_name = args.folder_name + '/'


##########lemmatize keywords############

file_text = open (folder_name + args.usecase_keywords,"r")
corpus = file_text.read().split('\n') # One word per line
print(len(corpus))
X = vectorizer.fit_transform(corpus) #dic of features

####### Lemmatized Topics ##############
topics_file = open(folder_name + args.topics,"r")
topic_lst = topics_file.read().split('\n')
topic = []
print (len(topic_lst))
for i in topic_lst[:-1]:
    topic.append(i.split(',')[1:][0])


doc_words = vectorizer.transform(topic)
arr_doc_words = doc_words.toarray()
notrelated_topics_indices = np.argwhere(doc_words.toarray().sum(1)==0)
print('#not-related emails-topics:%d', len(notrelated_topics_indices))
related_topics_indices = np.argwhere(doc_words.toarray().sum(1)>0)
print('#related emails-topics:%d', len(related_topics_indices))

arr_doc_words[related_topics_indices]


result = open (folder_name + args.output_related_topics,'w+')
for i in range(len(related_topics_indices)):
 item_1 = topic_lst[int(related_topics_indices[i])]
 result.write(str(item_1)+"\n")
result.close()
