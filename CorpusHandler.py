import nltk
import sys
import re
import os



#The txt tagged transcriptfiles are formatted in the way that the first word identifies the person
#and the second word identifies if it is a claim, premise or regular sentence. These two features
#are extracted and then deleted so that the normal sentence remains. 
def createArgList(path='Testcorpus\TaggedTCs'):
    biglist = []
    for filename in os.listdir(path):
        file = open(path + '\\' + filename, 'r')
        for line in file:
            splitsent = line.split(' ')
            person = splitsent[0]
            tag = splitsent[1]
            del splitsent[0]
            del splitsent[0]
            try:
                splitsent.remove('\n')
            except:
                pass
            sent = ' '.join(splitsent)
            biglist.append([person, tag, sent])
        file.close()
    return biglist






""" This method is not currently used in the classification process,but
creates a processed list of sentences with their tags from the Stab and
Gurevych corpus"""
def createStabArgList(path='Testcorpus\Stab', count=90):
    c=1
    biglist = []
    while c<=int(count):
        if len(str(c))==1:
            rawfilepath = path + '\essay0' + str(c) + '.txt'
            argfilepath = path + '\essay0' + str(c) + '.ann'
        else:
            rawfilepath = path + '\essay' + str(c) + '.txt'
            argfilepath = path + '\essay' + str(c) + '.ann'
        arglist = listcreator(rawfilepath, argfilepath)
        try:
            for tup in arglist:
                biglist.append(tup)
        except:
            pass
        c+=1
    outputlist = open('fullcorpuslist.txt', 'w')
    outputreadable = open('readablefullcorpus.txt', 'w')
    outputlist.write(str(biglist))
    for tup in biglist:
        outputreadable.write(str(tup))
        outputreadable.write('\n')
    outputlist.close()
    outputreadable.close()
    return biglist

"""This method adds an amount of non argumentative text to the list
, depending on the amount of argumentative sentences. In the end, the amount of regular sentences are
equal to the amount of argumentative sentences."""
def addNonArgText(biglist):
    addsentamt = 0
    amtreg=0
    for tup in biglist:
        if tup[1]!='Reg':
            addsentamt+=1
        else:
            amtreg+=1
    addsentamt-=amtreg
    brownsents = nltk.corpus.brown.sents(categories='news')
    c=0
    while c<len(brownsents) and addsentamt>0:
        sent=brownsents[c]
        sent = ' '.join(sent)
        sent = sent.replace(' ,', ',')
        sent = sent.replace(" '", "'")
        sent = sent.replace(' :', ':')
        sent = sent.replace(' ;', ';')
        sent = sent.replace(' .', '.')
        biglist.append([sent, 'Reg'])
        c+=1
        addsentamt-=1
    return biglist

        
def listcreator(rawtext, argtext):
    textfile = open(rawtext, 'r')
    arglist = handleArgFile(argtext)
    text = textfile.read()
    textfile.close()
    extendedlist = completeSentences(text, arglist)
    return extendedlist
"""Handles a .ann argumentation file of the Stab and Gurevych corpus (2014)
    The method extracts a list of arguments and their classification"""
def handleArgFile(argfile):
    file = open(argfile, 'r')
    args = file.read()
    file.close()
    arglist = args.split('\n')
    newlist = []
    for sentence in arglist:
        sentence = nltk.tokenize.word_tokenize(sentence)
        try:
            senttag = sentence[0]
            if senttag[0]=='T':
                resent = ' '.join(sentence[4:])
                c=0
                resent = resent.replace(" ,", ",")
                resent = resent.replace(" '", "'")
                newlist.append([resent, sentence[1]])
          
        except:
            pass
    return newlist

def completeSentences(text, arglist):
    splittext = re.split('\.|\?|\!', text)
    newlist = []
    for sentence in splittext:
        try:
            if sentence[0]== ' ':
                sentence = sentence[1:]
        except:
            pass
        argumentative = False
        for tup in arglist:
            if tup[0] in sentence:
                argumentative = True
                newsent = sentence.replace('\n', '')
                tup[0]=newsent
                newlist.append(tup)
        if argumentative == False:
            #This intercepts some weird empty sentence strings
            if len(sentence)>1:
                arglist.append([sentence,'Reg'])
    return arglist
