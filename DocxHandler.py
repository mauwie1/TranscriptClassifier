from docx import Document
import sys
import xlwt

def getText(filename):
    #Extracts the text from a docx document that contains tables
    transcript = Document(filename)
    textlist = []
    for table in transcript.tables:
        for row in table.rows:
            for cell in row.cells:
                textlist.append(cell.text)
    return textlist

def makeNormalTupleList(textlist):
    #Makes a list of tuples from a list of text,
    #The supported format is a docx file with in its first column the speaker,
    #indicated by 'P' or 'Person' followed by a number and in its second column
    #the spoken text. This is the standard format.
    tuplelist = []
    personOrText = 0
    element = 0
    while element <len(textlist):
        if personOrText == 0:
            person = returnPersonRegular(textlist[element])
            if element+1<len(textlist):
                tuplelist.append([textlist[element+1],person])
                personOrText = 1
        else:
             personOrText = 0
        element+=1
    return tuplelist

def makeTupleListDoctype1(textlist):
    #Within document type 1, the document starts with some information that is
    #irrelevant to argumentation. The actual discussion starts whenever the word
    #'recording' or 'Recording' occurs in a cell of the table. In addition, one
    #cell may abruptly end at the end of a page, which may result in a situation
    #where the speaker of the text is only indicated in the next row. 
    tuplelist = []
    startbool = False
    personOrText = 0
    element = 0
    while element+1<len(textlist):
        if startbool == True:
            if personOrText == 0:
                person = returnPersonRegular(textlist[element])
                # if the person is not in the format P1: or PERSON 1:, the program analyzes if the next row has an identifier.
                # This makes sure table rows at the end of a page that are split are merged and identified. However,
                # whenever that row does not also not contain an identifier, the rows are dropped.
                if person == 'Unknown' and element+3<len(textlist):
                    persontext = textlist[element]+textlist[element+2]
                    person = returnPersonRegular(persontext)
                    if person != 'Unknown':
                        celltext = textlist[element+1]+textlist[element+3]
                        tuplelist.append([celltext,person])
                    else:
                        element+=2
                elif person == 'Empty':
                        try:
                            tuplelist[element-1[0]]+=textlist[element]
                        except:
                            pass
                else:
                    tuplelist.append([textlist[element+1],person])
                personOrText = 1
            else:
                personOrText = 0
        else:
            if 'recording' in textlist[element] or 'Recording' in textlist[element]:
                startbool = True
        element+=1
    return tuplelist

def makeTupleListDoctype2(textlist):
    #Within document type 2, the document starts with irrelevant information for
    #argumentation. The discussion starts whenever the participants are identified
    #followed by a large amount of '='s, indicating a border. Within the first column
    #, only timestamps are present. The second column contains the person who speaks
    #and the actual text. The person is placed in front of the text like: 'P1:'
    tuplelist = []
    startbool = False
    celltype = 0
    element = 0
    textlist = improveTextlist(textlist)
    while element <len(textlist):
        celltext = textlist[element]
        if startbool == True:
            if celltype == 0:
                celltype = 1
            elif celltype == 1:
                celltype = 2
            else:
                celltextlist = returnTuples(celltext)
                for x in celltextlist:
                    tuplelist.append(x)
                celltype = 0
        else:
            if 'P1' in celltext:
                celltextchar = 0
                while celltextchar < len(celltext):
                    if celltext[celltextchar] == '=':
                        while celltext[celltextchar] == '=' or celltext[celltextchar].isspace():
                            celltextchar+=1
                        celltuplelist = returnTuples(celltext[celltextchar:])
                        for tuple in celltuplelist:
                            tuplelist.append(tuple)
                        break
                    celltextchar+=1
                startbool = True
        element+=1
    return tuplelist
                   
def returnPersonRegular(text, startchar=0):
    #Returns a person like 'P1' or 'Person1' from a textcell
    counter=startchar
    if len(text)==0:
        return 'Empty'
    while counter <len(text):
        if text[counter]=='R':
            break
        if text[counter].isalpha():
            return text[counter:]
        counter+=1
    return 'Unknown'

def returnTuples(text):
    #Returns a person like 'P1' or 'Person1' from a textcell
    tuplelist = []
    wordlist = text.split(' ')
    counter=0
    firsttext = wordlist[counter]
    firstlength = len(firsttext)
    person = firsttext[:firstlength-1]
    counter+=1
    while counter < len(wordlist):
        sentence = '' 
        while counter<len(wordlist) and ':' not in wordlist[counter]:
            sentence+=wordlist[counter]+' '
            counter+=1
        tuplelist.append([sentence, person])
        try:
            word = wordlist[counter]
            length = len(word)
            person=word[:length-1]
        except:
            pass
        counter+=1
    return tuplelist
        

def improveTextlist(textlist):
    newlist = []
    for sentence in textlist:
        sentencetext=''
        for char in sentence:
            if char == '\n':
                sentencetext+=' '
            else:
                sentencetext+=char
        for word in sentencetext:
            if word == 'coz' or word == 'Coz':
                word = 'because'
        newlist.append(sentencetext)
    return newlist

    
def decideDoctype(text):
    #Decides which format the document is in. Type 0 is the regular format 
    if text[0] == 'Respondent':
        return 1
    elif 'Timespan' in text[1]:
        return 2
    elif 'Recording' in text[1]:
        return 1
    else:
        return 0

def checkTupleList(tuplelist):
    #Checks whether each tuple contains a person as identifier by checking if the entry
    # is too long or not
    for tuple in tuplelist:
        person = tuple[1]
        if len(person)>15:
            return False
    return True
        
def handleFile(filename):
    #Returns a list of tuples from a docx file. The tuples' first entry is spoken text
    #and the second entry is a person identifier. 
    text = getText(filename)
    doctype = decideDoctype(text)
    tuplelist=[]
    if doctype == 0:
        tuplelist = makeNormalTupleList(text)
    if doctype == 1:    
        tuplelist = makeTupleListDoctype1(text)
    if doctype == 2:
        tuplelist = makeTupleListDoctype2(text)
    tuplebool = checkTupleList(tuplelist)
    if tuplebool == True:
        return tuplelist

if __name__ == "__main__":
    print(handleFile(sys.argv[1]))  
