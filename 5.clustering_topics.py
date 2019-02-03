import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
#vectorizer = CountVectorizer()

 To run
'''
python 5.clustering_topics.py [--folder_name 'folder'] [--related_topics_emails ''] [--usecase_keywords_lemmatized ''] [--eps ''] [--min_samples ''] [--max_choose 10]
'''

ef parse_args():
	'''
	Parses the arguments.
	'''
	parser = argparse.ArgumentParser(description="Run 5.clustering_topics.py")
        
	parser.add_argument('--folder_name', nargs='?', default='folder', help='input/output folder name')
	parser.add_argument('--related_topics_emails', nargs='?', default='related_topics_emails.txt', help='related topics file')
	parser.add_argument('--usecase_keywords_lemmatized', nargs='?', default='keywords_lemmatized.txt', help='Input keywords corpus')
	parser.add_argument('--eps', nargs='?', default=15, help='eps value for DBSCAN algorithm')
	parser.add_argument('--min_samples', nargs='?', default=1, help='minimum samples of each cluster in DBSCAN algorithm')
	parser.add_argument('--max_choose', nargs='?', default=10, help='minimum samples of each cluster in DBSCAN algorithmmax number of representative topics for each cluster')

        
        
         ####################
	return parser.parse_args()


args = parse_args()
folder_name = args.folder_name + '/'
eps = args.eps
vectoriz_source = 'keywords'
#vectoriz_source = 'topics'
folder_name ='result_98keywords/'
########## read the emails topics after the secondfiltering #######
file = os.path.join(folder_name + args.related_topics_emails)
topics_file = open (file,"r")
topic_lst = topics_file.read().split('\n')
topic = []
topic_mid = []
print (len(topic_lst))
for i in topic_lst[:-1]:
    topic.append(i.split(',')[1:][0])
    topic_mid.append(i.split(',')[:1][0])
print ('step : 1')
####### generate vectorize #########
file = os.path.join(folder_name+args.usecase_keywords_lemmatized)
file_text = open (file,"r")
keywords = file_text.read().split('\n') # One word per line
print('#keywords: %d',len(keywords))

####################################
#if vectoriz_source=='keywords':
#    X = vectorizer.fit_transform(keywords)
#    doc_words = vectorizer.transform(topic)
#    ep = 15
#else:
#    doc_words = vectorizer.fit_transform(topic)
#    ep= 3


sim_matrix = cosine_similarity(doc_words,doc_words)
print ('4.similarity done')
#### eps is similarity threshold, changes from 1 (low similarity) to 0 (high similarity) #######
db = DBSCAN(eps, min_samples=1).fit(sim_matrix)
print ('5.clustering done')

labels = db.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
print ('#clusters:%d' %  n_clusters)
print ('#clusters:%d' %  len(labels))

file = os.path.join(folder_name + 'related_mid.txt')
file_text = open (file,"r")
subjects_id = file_text.read().split('\n') # One id per line

clustered_topics = np.concatenate([[topic_mid],[labels]])
mid_cluster = np.transpose(clustered_topics)

np.savetxt(folder_name + "clustered_topic_after_2nd_filtering_"+vectoriz_source+".csv", mid_cluster, delimiter=",",fmt='%s')

print ('step : 7')
features = vectorizer.get_feature_names()
max_choose = args.max_choose
clusters_id = []
cluster_subjects = []
number_of_emails = []
for cluster_id in range(n_clusters):
    i_clusters = np.where(mid_cluster[:,1]==str(cluster_id))[0]
    sum_of_words_mat = doc_words[i_clusters][:].sum(0)
    sum_of_words_arr = np.array(sum_of_words_mat)
    max_nonzero = min(len(np.nonzero(sum_of_words_arr)[0]),max_choose)
    #print(max_nonzero)
    words_indx = sum_of_words_arr.argsort()[0][-max_nonzero:][::-1]
    cluster_words = [features[i] for i in words_indx]
    #print(cluster_words)
    clusters_id.append(cluster_id)
    cluster_subjects.append(cluster_words)
    number_of_emails.append(len(i_clusters))
#print(clusters_id)

print('number of clusters: %d',len(number_of_emails))
print('number of clusters: %d',len(clusters_id))
print('number of topic groups: %d',len(cluster_subjects))
#print(cluster_subjects)
clustered_topics = np.column_stack((clusters_id,number_of_emails,cluster_subjects))
#to_write = np.transpose(clustered_topics)
 

np.savetxt(folder_name + "clusters_representive_words_"+vectoriz_source+".csv", clustered_topics, delimiter=",",fmt='%s')

