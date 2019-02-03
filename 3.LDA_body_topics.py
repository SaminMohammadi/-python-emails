from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *
import numpy as np
import nltk
from nltk.corpus import stopwords
import settings
import gensim
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import argparse


# To run
'''
python 3.LDA_body_topics.py [--folder_name 'folder'] [--bodies_file ''] [--mid_file ''] [--related_bodies '']
'''

##################################
#########Input Arguments##########
##################################
def parse_args():
	'''
	Parses the arguments.
	'''
	parser = argparse.ArgumentParser(description="Run 3.LDA_body_topics.py")
        
	parser.add_argument('--folder_name', nargs='?', default='folder', help='input/output folder name')

	#parser.add_argument('--subjects_file', nargs='?', default='subjects_from_db.txt', help='Input subjects corpus')

	#parser.add_argument('--usecase_keywords', nargs='?', default='keywords.txt', help='Input keywords corpus')

	parser.add_argument('--bodies_file', nargs='?', default='body_from_db.txt', help='Input body corpus')

	parser.add_argument('--mid_file', nargs='?', default='related_mid.txt', help='Input mid corpus')
        ####################
	parser.add_argument('--related_bodies', nargs='?', default='related_bodies.txt', help='related bodies file')
        ####################
	return parser.parse_args()


args = parse_args()
folder_name = args.folder_name + '/'
##################################
######LEMMATIZATION FUNCTION######
##################################
def lemmatize_input_file(input_file, output_file):
 subject_file = input_file 
 subject_file_text = open (folder_name + subject_file,"r")
 subjects = subject_file_text.read().split('\n')
 print(len(subjects))
 lemmatized_subjects = open (folder_name + output_file,'w+')
 i=1
 for sentence in subjects:
        punctuations="?:!.,;"
        sentence_words = nltk.word_tokenize(sentence)
        for word in sentence_words:
            word = word.lower()
            if word in punctuations:
                sentence_words.remove(word)
        for word in sentence_words:
                word = word.lower() 
                wnl = WordNetLemmatizer()
                string = wnl.lemmatize(word, 'v')
                if word != string :
                    lemmatized_subjects.write(str(string)+" ")
                elif  word != wnl.lemmatize(word, 'n') :
                    string = wnl.lemmatize(word, 'n')
                    lemmatized_subjects.write(str(string)+" ")
                elif  word != wnl.lemmatize(word, 'r') :
                    string = wnl.lemmatize(word, 'r')
                    lemmatized_subjects.write(str(string)+" ")
                else:
                    string = wnl.lemmatize(word, 'a')
                    lemmatized_subjects.write(str(string)+" ")
        lemmatized_subjects.write("\n")

 lemmatized_subjects.close()

##################################
stopWords = set(stopwords.words('english'))

def preprocess_nltk_en(text):
    """ Remove puncuaitons in English text
    """
    result = []
    text = text.lower()
    text = ''.join(
        c for c in text if re.match("[a-z\-\' \n\t]", c)
    )
    tokens = nltk.word_tokenize(text)
    for token in tokens:
        if token not in stopWords:
            result.append(token.split())
    return result

##################################
def get_topic_top_words(lda_model, nr_top_words):
    """ Returns the top words for topic_id from lda_model.
    """
    id_tuples = lda_model.get_topic_terms(topn=nr_top_words,topicid=0)
    word_ids = np.array(id_tuples)[:,0]
    words = map(lambda id_: lda_model.id2word[id_], word_ids)
    return words

def get_topic_weight(lda_model):
    weight_topics = []
    for idx, topic in lda_model.print_topics():
        weight_topics.append('{}'.format(topic))
    return weight_topics

##################################
args = parse_args()

##################################

def main():
    lemmatize_input_file(args.related_bodies, 'related_bodies_lemmatized.txt')
######################################
    with open(folder_name + 'related_bodies_lemmatized.txt', encoding='utf-8') as data_file:
        topics_file = open(folder_name + 'output_topics.txt','w+')
        topics_file_weights = open(folder_name + 'output_topics_weight.txt','w+')
        mids = open(folder_name + args.mid_file).read().split('\n')
        print ('#mid: %d',len(mids))
        document = data_file.read()
        corpus = document.split('\n')
        print('#bodies: %d',len(corpus))
        
        for (body,mid) in zip(corpus,mids):
            processed_docs = preprocess_nltk_en(body)

            dictionary = gensim.corpora.Dictionary(processed_docs)
        

    # Bag of Words on the Data set
    # Create a dictionary from ‘processed_docs’ containing the number of times a word appears in the training set.
    # For each document we create a dictionary reporting how many words and how many times those words appear. Save this to ‘bow_corpus’, then check our selected document earlier.
            bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
            if len(bow_corpus)!= 0 :
                    LDA_model = gensim.models.LdaMulticore(corpus=bow_corpus,
                                          id2word=dictionary,
                                          num_topics=settings.num_topics)
            
        
                    ldamodel = gensim.models.ldamodel.LdaModel(bow_corpus, num_topics=settings.num_topics, id2word=dictionary)
                    top_words = get_topic_top_words(LDA_model, settings.no_of_top_words)
                    topics_file.write(mid+', '+format("  ".join(top_words))+"\n")
                    topics_file_weights.write(mid+","+", ".join(get_topic_weight(ldamodel))+"\n")




main()
