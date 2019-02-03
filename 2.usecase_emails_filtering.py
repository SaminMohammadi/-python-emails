import argparse
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


# To run
'''
python 2.usecase_emails_filtering.py [--folder_name 'folder'] [--usecase_keywords ''] [--output_related_subjects ''] [--output_related_bodies '']
'''


vectorizer = CountVectorizer()

import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()


##################################
#########Input Arguments##########
##################################
def parse_args():
	'''
	Parses the arguments.
	'''
	parser = argparse.ArgumentParser(description="Run 2.usecase_emails_filtering.py")
	parser.add_argument('--folder_name', nargs='?', default='folder', help='input/output folder')
        
	parser.add_argument('--subjects_file', nargs='?', default='subjects_from_db.txt', help='Input subjects corpus')

	parser.add_argument('--usecase_keywords', nargs='?', default='keywords.txt', help='Input keywords corpus')

	parser.add_argument('--bodies_file', nargs='?', default='body_from_db.txt', help='Input body corpus')

	parser.add_argument('--mid_file', nargs='?', default='mid_from_db.txt', help='Input mid corpus')
        ####################
	parser.add_argument('--output_related_subjects', nargs='?', default='related_subjects.txt', help='related subjects file')
	parser.add_argument('--output_related_subjects_lemmatized', nargs='?', default='related_subjects_lemmatized.txt', help='related subjects file lemmatized')
	parser.add_argument('--output_related_bodies', nargs='?', default='related_bodies.txt', help='related bodies file')
	parser.add_argument('--output_related_mid', nargs='?', default='related_mid.txt', help='related  mid file')
        ####################
	return parser.parse_args()


args = parse_args()
folder_name = args.folder_name + '/'

##################################
###### LEMMATIZATION FUNCTION ######
##################################
def lemmatize_input_file(input_file, output_file):
 subject_file = input_file 
 subject_file_text = open (folder_name+subject_file,"r")
 subjects = subject_file_text.read().split('\n')
 print(len(subjects))
 lemmatized_subjects = open (folder_name+output_file,'w+')
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

#Lemmatize subjects
lemmatize_input_file(args.subjects_file,'subjects_from_db_lemmatized.txt')

#lemmatize keywords
lemmatize_input_file(args.usecase_keywords,'keywords_lemmatized.txt')
file = os.path.join(folder_name+'keywords_lemmatized.txt')
file_text = open (file,"r")
corpus = file_text.read().split('\n') # One word per line
X = vectorizer.fit_transform(corpus) #dic of features


####### Lemmatized Subjects ##############
subject_file = os.path.join(folder_name+'subjects_from_db_lemmatized.txt')
subject_file_text = open (subject_file,"r")
subjects = subject_file_text.read().split('\n') # One subject  per line
##########################################

###### Non-Lemmatized Subjects ###########
subject_file_nonL = os.path.join(folder_name+args.subjects_file)
subject_file_text_nonL = open (subject_file_nonL,"r")
subjects_nonL = subject_file_text_nonL.read().split('\n') # One subject  per line
##########################################

###### mid Subjects ###########
subject_file_mid = os.path.join(folder_name+args.mid_file)
subject_file_text_mid = open (subject_file_mid,"r")
mid = subject_file_text_mid.read().split('\n') # One mid  per line
##########################################

doc_words = vectorizer.transform(subjects)
arr_doc_words = doc_words.toarray()
related_subjects_indices = np.argwhere(doc_words.toarray().sum(1)>0)
print('#related emails:%d', len(related_subjects_indices))

arr_doc_words[related_subjects_indices]


result_lem = open (folder_name+args.output_related_subjects_lemmatized,'w+')
result = open (folder_name+args.output_related_subjects,'w+')
result_mid = open (folder_name+args.output_related_mid,'w+')
for i in range(len(related_subjects_indices)):
 item_1 = subjects_nonL[int(related_subjects_indices[i])]
 item_2 = subjects[int(related_subjects_indices[i])]
 item_3 = mid[int(related_subjects_indices[i])]
 result.write(str(item_1)+"\n")
 result_lem.write(str(item_2)+"\n")
 result_mid.write(str(item_3)+"\n")

result.close()
result_lem.close()
result_mid.close()


body_file = os.path.join(folder_name+args.bodies_file)
body_file_text = open (body_file,"r")
bodies = body_file_text.read().split('\n') # One body in each line

result = open (folder_name+args.output_related_bodies,'w+')
for i in range(len(related_subjects_indices)):
 item_1 = bodies[int(related_subjects_indices[i])]
 result.write(str(item_1)+"\n")
 
result.close()




