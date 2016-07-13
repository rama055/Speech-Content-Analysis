
import urllib2
import re

#url = 'http://intelligencesquaredus.org/debates/past-debates/item/1333-the-equal-protection-clause-does-not-require-states-to-license-same-sex-marriages'

url = raw_input('Enter url from which comments are to be extracted: ')

source = urllib2.urlopen(url).read()
#num_of_comments = int(re.search('<h3 class="itemCommentsCounter"> <span>([0-9]?[0-9])</span>',source).group(1))
num_of_comments = int(re.search('<span>(.*)</span> comments ',source).group(1))
comments_section_list = source.split('class="commentAuthorName">')
comments = []
for i in range(1,len(comments_section_list)):
	if(re.search('posted by',str(comments_section_list[i]))!=-1):
		 c = re.search('</span><p>(.*)</p></li>',comments_section_list[i]).group(1)
                 c = c.replace('<br />','')
                 comments.append(c)
num_of_comments -= 20
if (num_of_comments > 0):
	iter = 0
	while (num_of_comments > 0) :
		
		next_url = url+'?start='+str((20 + iter * 20))	
		source = urllib2.urlopen(next_url).read()
		comments_section_list = source.split('class="commentAuthorName">')
		for i in range(1,len(comments_section_list)):
        		if(re.search('posted by',str(comments_section_list[i]))!=-1):
                		c = re.search('</span><p>(.*)</p></li>',comments_section_list[i]).group(1)
				c = c.replace('<br />','')
				comments.append(c)
		iter += 1
		num_of_comments -= 20

fp = open('comments.txt','w')
for comment in comments:
	fp.write(comment);
	fp.write("\n***********\n")
fp.close();
