import os
import pandas as pd
from striprtf.striprtf import rtf_to_text
import re
from tqdm import tqdm
import time

def collect_factiva(folder_name:str):
    print('Run folder...',os.path.basename(folder_name))
    count = 0
    # create an empty dataframe
    df = pd.DataFrame(columns=['GVKEY','File','Document','Date','Time','Words'])
    # read file from directory path
    for file_name in os.listdir(folder_name):
        try:
            path = os.path.join(folder_name, file_name)
            with open(path, 'r', encoding='utf8') as f:
                text = f.read()
            # convert rtf format to text
            text = rtf_to_text(text, errors='ignore')
    
            # split text by newline
            fulltext = []
            for i in text.split('\n'):
                if len(i) > 1:
                    fulltext.append(i)
    
            # collect data from each document nad doc_no.
            gvkey,from_file,doc_no = [],[],[]
            doc_list = []
            docs = []
            txt = []
            for i in fulltext:
                if not re.search("^Document [A-Za-z0-9]{25}",i):
                    txt.append(i)
                else:
                    doc_no.append(i)
                    doc_list.append(txt)    # to use in next step collection
                    sum_txt = '\n'.join(txt)     # combine elements in a data list as text. 
                    docs.append(sum_txt)
                    gvkey.append(os.path.basename(folder_name))
                    from_file.append(file_name)
                    txt = []
                    
                    
            # collect num_words, date, time, and doc_no.
            num_words,date,time = [],[],[]
            for doc in doc_list:
                if len(doc) > 5:
                    for i in range(len(doc)):
                        if re.search("[\d]+[\s]words$", doc[i]) and re.search("^[0-9]{1,2}[\s][\w]+[\s][0-9]{4}$", doc[i+1]) and re.search("^[\d]{2}:[\d]{2}$", doc[i+2]):
                            num_words.append(doc[i])
                            date.append(doc[i+1])
                            time.append(doc[i+2])
                        elif re.search("[\d]+[\s]words$", doc[i]) and re.search("^[0-9]{1,2}[\s][\w]+[\s][0-9]{4}$", doc[i+1]) and not re.search("^[\d]{2}:[\d]{2}$", doc[i+2]):
                            if re.search("[\d]{2}:[\d]{2}:[\d]{2}",doc[i-1]):
                                num_words.append(doc[i])
                                date.append(doc[i+1])
                                time.append(re.search("[\d]{2}:[\d]{2}",doc[i-1])[0])
                            else:
                                num_words.append(doc[i])
                                date.append(doc[i+1])
                                time.append("-")
                else:
                    num_words.append("-")
                    date.append("-")
                    time.append("-")
    
    
            # append the dataframe of each file_name's data
            df = df.append(pd.DataFrame({'GVKEY':gvkey,
                                         'Document':doc_no,
                                         'File':from_file,
                                         'Date':date,
                                         'Time':time,
                                         'Words':num_words,
                                         'Data':docs}), ignore_index=True)
    
            count += 1
            print(count,'/',len(os.listdir(folder_name)),'processing...')
            print(file_name,'Done...')
        except:
            file_error.append(str(os.path.basename(folder_name)+file_name))
    print('----------------------------------------------------------------------')
    return df.to_excel(os.path.basename(folder_name) +'.xlsx',index=False)

# check file in onedrive shortcut
onedrive_path = 'C:\\Users\\Alpha 15 A3DD\\OneDrive - Chiang Mai University\\News Data'
onedrive_folder = []
for i in os.listdir(onedrive_path):
    onedrive_folder.append(i)
# print(len(onedrive_folder))
# print(onedrive_folder[-1]) #desktop.init
# print(len(onedrive_folder[:-1]))

# to keep error file
file_error = []

# convert to csv...
start = time.time()
for i in tqdm(onedrive_folder[:-1]):
    onedrive_folder_path = os.path.join(onedrive_path,i)
    collect_factiva(onedrive_folder_path)
stop = time.time()

print('End of process...', stop-start, 'sec')


########################################################
df_error = pd.DataFrame({'filename':file_error})
df_error.to_excel('list_error_file.xlsx', index=False)



