import subprocess
import os
import pickle

path_360 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/360p processed/'
path_720 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/720p processed/'
path_list=[path_360,path_720]
all_lines = []
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
                        for line in lines:
                                if(line!= '' ):
                                        all_lines.append(line.split(' '))
		cf = subprocess.Popen(["ls comments.txt"],shell=True,stdout=subprocess.PIPE)
		cfiles,err = cf.communicate()
		cfiles = cfiles.split('\n')	
		cfiles.remove('')
		for file in cfiles:
			cfh = open(file,'r')
			content = cfh.read()
			content = content.replace('\n***********\n','')
			lines = content.split('.')
			for line in lines:
				if(line!= '' ):
                                        all_lines.append(line.split(' ')) 
file = open('/Users/AbhishekSharmaRamachandra/DR/code/all_lines','a+')
pickle.dump(all_lines,file)
file.close()
