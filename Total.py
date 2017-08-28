import sys
import CorpusHandler
import Machinelearn
import DocxHandler
import TextHandler
import Features
import KeywordFeatures as kf

tcpath = 'Tcs\\'
def classify(tc):
    #arglist is the list of argumentational text sentences on which the classifier is trained
    #combined with the document separation lines.
    arglist = CorpusHandler.createArgList()
    tuplelist = DocxHandler.handleFile(tcpath + tc + '.docx')
    tuplelist = TextHandler.handleText(tuplelist, 4)
    classifier = Machinelearn.TCsArgTraining(arglist)
    guesslist = []
    c=0
    while c <len(tuplelist):
        tup = tuplelist[c]
        sent = tup[0]
        #It is appended before the guess occurs, because one feature needs to evaluate
        #the current speaker
        guesslist.append([tup[1], '', sent])
        guess = classifier.classify(Features.TCsFeatures(sent, c, guesslist))
        guesstup = guesslist[c]
        guesstup[1]=guess
        c+=1
    #It classifies the text two times more, but these times with two added features that rely on
    #an already classified text. These features involve if one the next sentences has the
    #same classification.
    file = open(tc +'_Arguments.txt', 'w')
    c=0
    while c <len(tuplelist):
        tup = tuplelist[c]
        sent = tup[0]
        guess = classifier.classify(Features.TCsFeatures(sent, c, guesslist, True))
        guesstup = guesslist[c]
        guesstup[1]=guess
        c+=1
    #In the last run, this method writes the guesses of the classifier to a file, only when it
    #guesses that the text is argumentative.
    c=0
    while c <len(tuplelist):
        tup = tuplelist[c]
        sent = tup[0]
        guess = classifier.classify(Features.TCsFeatures(sent, c, guesslist, True))
        if guess!='Reg':
            file.write(guess+' '+sent + '\n')
        c+=1
    file.close()

if __name__ == "__main__":
    classify(sys.argv[1])


