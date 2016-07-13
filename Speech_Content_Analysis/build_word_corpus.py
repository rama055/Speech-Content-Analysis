import subprocess
import os
import pickle

word_dict = {};
comments_file = 'comments.txt'
path_360 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/360p processed/'
path_720 = '/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/720p processed/'
path_list=[path_360,path_720]
for path in path_list:
	os.chdir(path)
	p = subprocess.Popen(["ls"],shell=True,stdout=subprocess.PIPE)
	debate_list, err = p.communicate()
	debate_list = debate_list.split('\n')
	debate_list.remove('')
	for debate in debate_list:
		debate_ID = debate.split(' ')[0]
		debate_path = path+debate 
		os.chdir(debate_path)
                f = subprocess.Popen(["ls split*"],shell=True,stdout=subprocess.PIPE)
                file_list,err = f.communicate()
                file_list = file_list.split('\n')
                file_list.remove('')
                for file in file_list:
                        speaker_ID = file.split("_")[2]
                        closeOrOpen = (file.split("_")[3]).split('.')[0]
                        file_handle = open(file,'r')
                        file_content = file_handle.read()
                        paragraphs = file_content.split('EOP')
                        paragraph_count = 0
                        for para in paragraphs:
                                paragraph_count += 1
                                lines = para.split('\n')
                                line_count = 0
                                for line in lines:
                                        if line == '':
                                                continue;
                                        line_count += 1
                                        word_list = line.split(' ')
                                        word_count = 0
                                        for word in word_list:
                                                if word != '':
                                                        word_count += 1
                                                        attr_dict = {'Debate_ID':debate_ID,'Speaker_ID':speaker_ID,'CloseOrOpen':closeOrOpen,'paragraph':paragraph_count,'line':line_count,'word':word_count}
                                                        word_dict [word] = attr_dict

                        file_handle.close()

		cf = open(comments_file,'r')
                comments = cf.read()
		comments = comments.replace('***********','')
		comments = comments.replace('\n***********','')
		comments = comments.replace('\n***********\n','')
                comments = comments.split('.')
                for comment in comments:
                        if comment != '' and comment != '\n':
                                word_list = comment.split(' ')
                                for word in word_list:
					attr_dict = {'Debate_ID':debate_ID,'Speaker_ID':'NA','CloseOrOpen':'NA','paragraph':'NA','line':'NA','word':'NA'}
					word_dict[word] = attr_dict		
fh = open('/Users/AbhishekSharmaRamachandra/DR/code/word_corpus','a+')
pickle.dump(word_dict,fh)
fh.close()

