
import subprocess
import os
change_directory_choice = raw_input('Current path of lookup for files: /Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/ \n\
1.Continue with this path\n\
2.Change Path\n')

if change_directory_choice == '1':
        relative_path = raw_input('Enter path to file relative to base lookup path: ')
        baseDirectory='/Users/AbhishekSharmaRamachandra/Desktop/DR/Public Speaking 2014  Intelligence^2/'
elif change_directory_choice == '2':
        baseDirectory = raw_input('Enter base path for lookup: ')
        relative_path = raw_input('Enter path to file relative to base lookup path: ')

file_choice=raw_input('1.Read specific file in directory\n\
2.Read all text files in current directory \n')
if file_choice == '1':
	file_name = raw_input('Enter filename: ')
        absolute_path = baseDirectory+relative_path+file_name
        my_file = open(absolute_path,'r')
                      
        transcript_text = my_file.read()
        my_file.close()
        paragraphs = transcript_text.split("\n")
        lines = []
        for paragraph in paragraphs:
     	   lines.append(paragraph.split('.'))
       	   #add delimiter between paragraphs
           lines.append('EOP')
	file= open('split_'+file_name,'w')
	for para in lines:
		if(para == 'EOP'):
			file.write('EOP\n\n')
		else:
			for line in para:
				file.write(line)
				file.write('\n\n')
	file.close()


elif file_choice ==  '2':
	path =  baseDirectory+relative_path
	os.chdir(path)
	p = subprocess.Popen(["ls *.txt"],shell=True,stdout=subprocess.PIPE)
        file_list, err = p.communicate()
	file_list=file_list.split('\n')
	file_list.remove('')
	file_dict = {} 
        for file in file_list:
	     if(file == 'comments.txt'):
		continue
             absolute_path = baseDirectory+relative_path+file
             my_file = open(absolute_path,'r')
                      
             transcript_text = my_file.read()
             my_file.close()
             paragraphs = transcript_text.split("\n")
             file_dict[file] = []
             for paragraph in paragraphs:
		     file_dict[file].append(paragraph)
	final_file_dict = {}
        for file in file_dict:
	     final_file_dict[file] = []
	for file in file_dict:
	     for para in file_dict[file]:
		     final_file_dict[file].append(para.split('.'))
		     final_file_dict[file].append("EOP")
	for file_name in final_file_dict:
		file = open('split_'+str(file_name),'w')
		for para in final_file_dict[file_name]:
			if(para == 'EOP'):
				file.write('EOP\n\n')
			else:
				for line in para:
					file.write(line)
					file.write('\n\n')
		file.close()
		
