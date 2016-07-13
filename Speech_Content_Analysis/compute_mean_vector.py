import re
import subprocess
import os
import pickle
import numpy as np
import csv
from gensim.models import Word2Vec

model=Word2Vec.load("all_words.model")
csvh=open('avg_vec.csv', 'wb')
csv_writer=csv.writer(csvh,delimiter=',')
path_360 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/360p processed/'
path_720 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/720p processed/'
path_list=[path_360,path_720]
avgVec={}
for path in path_list:
        os.chdir(path)
        p = subprocess.Popen(["ls"],shell=True,stdout=subprocess.PIPE)
        debate_list, err = p.communicate()
        debate_list = debate_list.split('\n')
        debate_list.remove('')
        for debate in debate_list:
		debate_path = path+debate
                os.chdir(debate_path)
                f = subprocess.Popen(["ls split*"],shell=True,stdout=subprocess.PIPE)
                file_list,err = f.communicate()
                file_list = file_list.split('\n')
                file_list.remove('')
                for file in file_list:
                        fh = open(file,'r')
                        file_content = fh.read()
                        file_content = file_content.replace('EOP','\n')
                        file_content = file_content.replace('\r','\n')
                        lines = file_content.split('\n')
			line_num=1
                        for line in lines:
				mod_words=[]
				vector=np.zeros(shape=(1,300))
                                if(line!= '' ):
                                        words=line.split(' ')
                                        for word in words:
                                                mod_word=re.sub('[^a-zA-Z]',"",word)
                                                if(mod_word!=""):
							vector = vector + model[mod_word]
					key=debate+","+file.split('_')[2]+","+file.split('_')[3].split('.')[0]+","+str(line_num)
					avgVec[key]={'Average Vector':vector}
					debateID=int(debate.split(" ")[0])
					speaker=int(file.split('_')[2].split("S")[1])
					opening=1
					if(file.split('_')[3].split('.')[0] == "C"):
						opening=0
					list=[]
					for x in vector:
						for y in x:
							list.append(y)
					row=[debateID,speaker,opening,line_num]
					row.extend(list)
					csv_writer.writerow(row)	
					line_num=line_num+1
			fh.close()

csvh.close()
avgFile=open("/Users/AbhishekSharmaRamachandra/DR/code/average_vectors",'w')
pickle.dump(avgVec,avgFile)
avgFile.close()
