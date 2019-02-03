import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer



# To run
'''
python 6.clusters_recipients.py [--folder_name 'folder'] [--recipients ''] [-clustered_topics ''] 
'''

##################################
#########Input Arguments##########
##################################
def parse_args():
	'''
	Parses the arguments.
	'''
	parser = argparse.ArgumentParser(description="Run 6.clusters_recipients.py")
        
	parser.add_argument('--folder_name', nargs='?', default='folder', help='input/output folder name')
	parser.add_argument('--recipients', nargs='?', default='recipients.txt', help='recipients list')

	parser.add_argument('--clustered_topics', nargs='?', default='clustered_topic_after_2nd_filtering_keywords.csv', help='clustered topics')

	####################
	return parser.parse_args()


args = parse_args()
folder_name = args.folder_name + '/'


vectorizer_sender = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
vectorizer_recipients = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)

vectoriz_source = 'keywords'
#vectoriz_source = 'topics'
###### read recipients information ######
file = os.path.join(folder_name + args.recipients)
recipients_str = open(file, "r")
sender_recipients = recipients_str.read().split('\n')

file = os.path.join(folder_name + 'mid_recipients.txt')
recipients_str = open(file, "r")
mid_recipients = recipients_str.read().split('\n')

###### separate sender & recipients ####
sender = [i.split(',')[:1] for i in sender_recipients]
recipients = [i.split(',')[1:] for i in sender_recipients]
########################################

###### read clusters #######
file = os.path.join(folder_name + args.clustered_topics)
file_str = open(file, "r")
clusters_mid = file_str.read().split('\n')
mid = [i.split(',')[0] for i in clusters_mid]
cluster = [i.split(',')[1] for i in clusters_mid]

clustered_messages = np.concatenate([[mid],[cluster]])
mid_cluster = np.transpose(clustered_messages)
########################################

max_choose = 10
clusters_id = []
cluster_senders = []
cluster_recipients = []
number_of_emails = []

X_senders = vectorizer_sender.fit_transform(sender)
X_recipients = vectorizer_recipients.fit_transform(recipients)
features_sender = vectorizer_sender.get_feature_names()
features_recipients = vectorizer_recipients.get_feature_names()

n_clusters = max([int(i) for i in cluster])
print(n_clusters)



for cluster_id in range(n_clusters):
    # indices of clustered messages 
    indx = np.where(mid_cluster[:,1]==str(cluster_id))[0]

    messages_id= [i for i in mid_cluster[indx,0]]
    intersect = list(set(messages_id).intersection(set(mid_recipients)))
    
    i_clusters = [np.where(np.transpose(mid_recipients)==str(i))[0][0] for i in intersect]
    # indices of the above messages 
    ######### Senders ##########
    sum_of_words_mat = X_senders[i_clusters][:].sum(0)
    sum_of_words_arr = np.array(sum_of_words_mat)
    max_nonzero = min(len(np.nonzero(sum_of_words_arr)[0]),max_choose)
    senders_indx = sum_of_words_arr.argsort()[0][-max_nonzero:][::-1]
    cluster_words = [features_sender[i] for i in senders_indx]
    clusters_id.append(cluster_id)
    cluster_senders.append(cluster_words)
    ######## Recipients ########
    sum_of_words_mat = X_recipients[i_clusters][:].sum(0)
    sum_of_words_arr = np.array(sum_of_words_mat)
    max_nonzero = min(len(np.nonzero(sum_of_words_arr)[0]),max_choose)
    recipients_indx = sum_of_words_arr.argsort()[0][-max_nonzero:][::-1]
    cluster_words = [features_recipients[i] for i in recipients_indx]
    cluster_recipients.append(cluster_words)
    ###########################
    number_of_emails.append(len(i_clusters))

clustered_senders = np.column_stack((clusters_id,number_of_emails,cluster_senders))
clustered_recipients = np.column_stack((clusters_id,number_of_emails,cluster_recipients))

np.savetxt(folder_name + "clusters_senders.csv", clustered_senders, delimiter=",",fmt='%s')
np.savetxt(folder_name + "clusters_recipients.csv", clustered_recipients, delimiter=",",fmt='%s')



