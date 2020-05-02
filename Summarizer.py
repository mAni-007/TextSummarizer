import urllib
import re
import nltk
import bs4
import heapq
import os
nltk.download('stopwords')


#Getting the data
source = urllib.urlopen('https://en.wikipedia.org/wiki/Harry_Potter')

soup = bs4.BeautifulSoup(source,'lxml')

text = ''
for paragraph in soup.find_all('p'):
	text += paragraph.text

#Creating a file for sentence storing ans summary storing
sen_file = open('Document', 'w+')
summary_file = open('Summary', 'w+')


#Preprocessing the text
text = re.sub(r'\[[0-9]*\]', ' ', text)
text = re.sub(r'\s+', ' ', text)
clean_text = text.lower()
clean_text = re.sub(r'\W', ' ',clean_text)
clean_text =  re.sub(r'\d', ' ',clean_text)
clean_text = re.sub(r'\s+', ' ', clean_text)

sen_file.write(clean_text)
sen_file.close()

#Not clean_text because it does not content any fullstop
sentences = nltk.sent_tokenize(text)	
# print(clean_text, len(clean_text))


#used so that no most occuring english comes as count
stop_words = nltk.corpus.stopwords.words('english')


#Creating histogram of words
word2count = {}
for word in nltk.word_tokenize(clean_text):
	if word not in stop_words:
		if word not in word2count.keys():
			word2count[word] = 1
		else:
			word2count[word] += 1

#Creating the weighted Histogram
for key in word2count.keys():
	word2count[key] = (word2count[key])/float(max(word2count.values()))

# print word2count

#Histogram of a sentences
sent2score = {}
for sentence in sentences:
	for word in nltk.word_tokenize(sentence.lower()):
		if word in word2count.keys():
			if len(sentence.split(' ')) < 25:
				if sentence not in sent2score.keys():
					sent2score[sentence] = word2count[word]
				else:
					sent2score[sentence] += word2count[word]
print (len(text))
best_sentence = heapq.nlargest(50, sent2score,key = sent2score.get)


print('----------------')
for sentence in best_sentence:
	summary_file.write(sentence.encode('utf-8'))

summary_file.close()