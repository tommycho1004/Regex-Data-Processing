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
        stringList = (line.lower().split(' ')) #convert everything to lowercase and split by white space
        for string in stringList:
            if string.replace('_', '').isalnum(): #check for alphanumeric with exception of underscore 
                wordList.append(string) #append to newlist
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

# create list with files
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