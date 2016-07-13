
import pickle
import gensim

file = open('all_lines','r')
all_lines = pickle.load(file)

model = gensim.models.Word2Vec( alpha=0.05,min_alpha=0.05, size=300, window=8, min_count=1, workers=4)
model.build_vocab(all_lines)
 
for epoch in range(50):
    model.train(all_lines)
    model.alpha -= 0.001  # decrease the learning rate
    model.min_alpha = model.alpha  # fix the learning rate, no decay
model.save('/Users/AbhishekSharmaRamachandra/DR/code/all_words.model')


