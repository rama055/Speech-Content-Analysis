from gensim.models.doc2vec import Doc2Vec
from gensim.models.doc2vec import LabeledLineSentence

sentences = LabeledLineSentence('/Users/scherer/Dropbox/Postdoc Work/DCAPS/data/all_utterances_total.txt')
# model = Doc2Vec(sentences, size=10, window=8, min_count=5, workers=4)


model = Doc2Vec(alpha=0.05, min_alpha=0.05, size=300, window=8, min_count=5, workers=4)  # use fixed learning rate
model.build_vocab(sentences)
 
for epoch in range(50):
    model.train(sentences)
    model.alpha -= 0.001  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save('/Users/scherer/Dropbox/Postdoc Work/DCAPS/data/WoZAIUtterances_total.model')

count=0
while (count< 290):
	var=model['SENT_'+str(count)]
	count=count+1
	fout=open('/Users/scherer/Dropbox/Postdoc Work/DCAPS/data/WoZAIUtterances_total.csv',"a")
	outString = ""
	for num in var:
		outString=outString+str(num)+","
	outString=outString[0:-1]
	fout.write(outString+"\n")