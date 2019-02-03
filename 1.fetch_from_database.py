import os
import pymysql.cursors
import mysql.connector
import argparse


# To run
'''
python 1.fetch_from_database.py [--folder_name 'folder']
'''


##################################
#########Input Arguments##########
##################################
def parse_args():
	 parser = argparse.ArgumentParser(description="Run 1.fetch_from_database.py")
	 parser.add_argument('--folder_name', nargs='?', default='folder', help='result folder')
         
	 return parser.parse_args()

args = parse_args()
folder_name = args.folder_name


##################################
#########SQL Connections##########
##################################
Enron_DB_cnnStr = pymysql.connect(host = "localhost",user = "root", passwd = "rootroot",database = "Enron")
Enron_DB_crsr = Enron_DB_cnnStr.cursor ()

Enron_DB_cnnStr1 = mysql.connector.connect(host = "localhost",user = "root", passwd = "rootroot",database = "Enron")
Enron_DB_crsr1 = Enron_DB_cnnStr1.cursor ()


##################################
###########SQL Scripts############
##################################
subjects_query = """select mid, replace(replace(replace(replace(body,'\r\n',''),'\n',''),'\\n',''),'\r',''), case  when substring(subject,1,3)= 're:' then substring(subject, 5) when substring(subject,1,4)= 'fwd:' then substring(subject, 6) when substring(subject,1,9)= 'fwd: fwd:' then substring(subject, 10)  when substring(subject,1,3)= 'fw:' then substring(subject, 5) when substring(subject,1,7)= 'fw: fw:' then substring(subject, 8)  when substring(subject,1,7)= 'fw: re:' then substring(subject, 8)   when substring(subject,1,7)= 're: fw:' then substring(subject, 8) when substring(subject,1,12)= 'fw: fw: re: ' then substring(subject, 13) when substring(subject,1,12)= 'fw: fw: fw:' then substring(subject, 13) when substring(subject,1,16)= 'fw: fw: fw: fw:' then substring(subject, 17) else subject end   from (select mid,body,subject from message where subject<>'' and subject<>'Re:' and body not like '<html><head><title>%' and body is not null and trim(body) <>'' order by mid desc) as a  """

mid_query = """select mid from (select mid,subject from message where subject<>'' and subject<>'Re:' and body not like '<html><head><title>%' order by mid desc) as a"""
mid__re_fw_query = """select mid, case  substring(subject,1,3) when 're:' then 1  when 'fw:' then 2 else 0 end  from (select mid,subject from message where subject<>'' and subject<>'Re:' and body not like '<html><head><title>%' and body is not null and trim(body) <>'' order by mid desc) as a"""

body_query = """select body from (select mid,body from message where subject<>'' and subject<>'Re:' and body not like '<html><head><title>%' and body is not null and trim(body) <>'' order by mid desc) as a"""

recipients_query = """select  recipientinfo.mid,b.eid, group_concat(distinct a.eid) recipient  from Enron.recipientinfo inner join message on message.mid=recipientinfo.mid 
inner join employeelist a on a.Email_id=recipientinfo.rvalue 
inner join employeelist b on b.Email_id=message.sender 
where subject<>'' and subject<>'Re:' and body not like '<html><head><title>%' and body is not null and trim(body) <>'' group by mid order by recipientinfo.mid desc"""


##################################
############Functions#############
##################################
def sending_query1(query_name,file_name):
	result = open (file_name,'w+')
	if query_name =='recipients_query':
	        Enron_DB_crsr1.execute(query_name)
	        ids = Enron_DB_crsr1.fetchall()
	else:
	        Enron_DB_crsr.execute(query_name)
	        ids = Enron_DB_crsr.fetchall()
	#ids = Enron_DB_crsr.fetchall()
        #print (len(ids))
	
	for i in range(len(ids)):
		
		id_info = ids[i]
		item_1 = id_info[0]
		#print (item_1)
		
		result.write(str(item_1)+"\n")		
	result.close()

def sending_query2(query_name,file_name,file2):
	result = open (file_name,'w+')
	result2 = open (file2,'w+')
	Enron_DB_crsr.execute(query_name)    
	ids = Enron_DB_crsr.fetchall()
        #print (len(ids))
	
	for i in range(len(ids)):
		
		id_info = ids[i]
		item_1 = id_info[0] #mid
		item_2 = id_info[1] #sender
		item_3 = id_info[2] #recipients
		#print (item_1)
		
		result.write(str(item_2)+','+str(item_3)+"\n")
		result2.write(str(item_1)+"\n") #mid
	result.close()


def sending_query3(query_name,file1,file2, file3):
        mid_result = open (folder_name + '/' + file1,'w+')
        body_result = open (folder_name + '/' + file2,'w+')
        subject_result = open (folder_name + '/' + file3,'w+')
        Enron_DB_crsr.execute(query_name)
        ids = Enron_DB_crsr.fetchall()
        for i in range(len(ids)):
                id_info = ids[i]
                item_1 = id_info[0]
                item_2 = id_info[1]
                item_3 = id_info[2]

                mid_result.write(str(item_1)+"\n")
                body_result.write(str(item_2)+"\n")
                subject_result.write(str(item_3)+"\n")
        mid_result.close()
        body_result.close()
        subject_result.close()
        

#sending_query1(subjects_query,folder_name+'subjects_from_db.txt')
#sending_query1(mid_query,folder_name+'mid_from_db.txt')
#sending_query1(mid_query,folder_name+'mid_re_fw_from_db.txt')
#sending_query1(body_query,folder_name+'body_mid_from_db.txt',folder_name+'body_from_db.txt')
sending_query3(subjects_query,'mid_from_db.txt','body_from_db.txt','subjects_from_db.txt')
sending_query2(recipients_query,folder_name + '/' +'recipients.txt',folder_name + '/' +'mid_recipients.txt')







