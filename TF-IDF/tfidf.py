# Tommy Cho, Jennifer Xin
import re
import math

# ----- TFIDF Problem -----


def clean(fileName):
# Helper method that splits the file into words that are strictly alphanumeric with the exception of underscore "_"
# parameter fileName: a string of the file being worked on
# return: a list of words (strings) that are stricitly alphanumeric with the exception of underscore
    stringList = []
    wordList = []
    pf = open(fileName, 'r')
    allOfIt = pf.readlines()
    pf.close()
    for line in allOfIt:
        stringList = (line.lower().split(' ')) #convert to lowercase
        for string in stringList:
            if not string.startswith('http://') or string.startswith('https://'): #check for website links
                if string != '': #handle whitespaces created by the split
                    wordList.append(re.sub(r'[^\w]','',string)) #use regex to remove all nonword characters
    return wordList

def stopWords(list):
# Helper method that removes stopwords from the word list
# parameter list: list of words being processed
# return: list of words without stopwords
    stopList = []
    outputList = []
    pf = open('stopwords.txt')
    stopwords = pf.readlines() 
    for word in stopwords:
        stopList.append(word.strip()) #create list of stopwords
    outputList = [word for word in list if word not in stopList] #use list comprehension to find difference of lists
    return outputList

def stemLemming(list):
# A helper method to stem and lemm (idk if that's a word) the word list
# parameter list: list of words being processed
# return: list of words that are stemmed and lemminized
    outputList = []
    for word in list:
    #if words end with a certain character sequence, simply remove that character sequence
        if word.endswith('ing'): 
            word = word[:len(word)-3] 
        elif word.endswith('ly'):
            word = word[:len(word)-2]
        elif word.endswith('ment'):
            word = word[:len(word)-4]
        outputList.append(word)
    return outputList

#TF-IDF calculations
def tf (file):
# Calculates the Term Frequency (TF) of each word in file
# Input: preprocessed file
# Output: Dictonary of word to TF
    pf = open(file,'r')
    words = [] # create a list with all of the words in file
    for r in pf.read().split():
        words.append(r)
    num_words = len(words)
    words.sort()
    res = {} # create a dictionary of unique words and their occurances in words
    for word in words:
        if word not in res:
            res[word] = 1
        else:
            res[word] += 1
    for ele in res.keys(): # calculate TF in TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
        res[ele] = res[ele] / num_words
    pf.close()
    return res

def top_five (tfidf):
# Gets the top 5 words with the highest TFIDF score
# Input: Dictionary of word to TFIDF score
# Output: List of 5 tuples in the format (word, TFIDF score)
    five = sorted(tfidf, key=tfidf.get, reverse=True)[:5]
    res = []
    for ele in five:
        res.append((ele,tfidf[ele]))
    return res

#main code to run
pf = open("tfidf_docs.txt", "r")
fileList = []
for r in pf:
    fileList.append(r.strip())
pf.close()
title = 'preproc_'
for file in fileList: #clean every file on the list
    print(file)
    cleanedList = clean(file)
    noStopWordList = stopWords(cleanedList)
    finishedList = stemLemming(noStopWordList)
    outputFile = open(title+file, 'w') #write the processed words onto new file
    outputFile.write(' '.join(finishedList))
    outputFile.close()


# Main code to run TF-IDF
num_docs = len(fileList)
set = {}
idf = {}
tfidf = {}
# idf = set.copy() only gives a shallow copy that references original so its useless
# instead I will create the lists with the files as keys
# calculate the TF nested dictionary first
for file in fileList:
    set[file] = tf(title+file)
    idf[file] = {}
    tfidf[file] = {}

#IDF calculation
# need a list of all unique words across all of the documents
all_words = []
for file, v in set.items():
    for key in v:
        if key not in all_words:
         all_words.append(key)
for word in all_words:
    count = 0
    for file in fileList:
        if word in set[file]:
            count += 1
    for key in set.keys():
        if word in set[key]:
            idf[key][word] = count
for file, v in idf.items():
    for word in v:
        idf[file][word] = math.log(num_docs / idf[file][word]) + 1
for file, v in set.items():
    for word in v:
        tfidf[file][word] = round(set[file][word] * idf[file][word], 2)
# calculating top 5 words of each file and outputting to the output files
prefix = 'tfidf_'
for file in fileList:
    top_5 = top_five(tfidf[file])
    output = open(prefix+file, 'w')
    output.write(str(top_5))
    output.close()