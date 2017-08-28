#Filters sentences that contain less words than a given threshold
def smallSentenceFilter(tuplelist, length):
    counter=0
    while counter<len(tuplelist):
        sentencetuple = tuplelist[counter]
        splitsentence = sentencetuple[0].split(' ')
        counter2=0
        while counter2<len(splitsentence):
            try:
                splitsentence.remove('')
            except:
                pass
            counter2+=1
        if len(splitsentence)<length:
            del tuplelist[counter]
            counter-=1
        counter+=1
    return tuplelist

#Converts paragraphs of text into individual sentences
def sentenceConverter(tuplelist):
    newlist = []
    for tuple in tuplelist:
        sentence = ''
        words = 0
        cell = tuple[0].split(' ')
        counter =0
        while counter< len(cell):
            word = cell[counter].lower()
            sentence+=word+' '
            words+=1
            if counter==len(cell)-1:
                newlist.append([sentence, tuple[1]])
                break
            if '.' in sentence or '?' in sentence:              
                newlist.append([sentence, tuple[1]])
                sentence=''
                words=0
            counter+=1
    return newlist

#Filters words that are common in transcripts and not useful
def textCleanup(tuplelist):
    for tuple in tuplelist:
        sent = tuple[0].split(' ')
        c=0
        while c<len(sent):
            if sent[c]=='coz' or sent[c]=='cause':
                sent[c]='because'
            elif sent[c]=='yeah':
                del sent[c]
                c-=1
            elif sent[c] == '[inaudible]':
                del sent[c]
                c-=1
            c+=1
        tuple[0]= ' '.join(sent)
    return tuplelist

#returns a list without non alpha characters such as commas
def prepWordList(sentence):
    wordlist = sentence.split(' ')
    newlist = []
    for word in wordlist:
        wordedit = ''
        for char in word:
            if char.isalpha()== True:
                wordedit+=char.lower()
        newlist.append(wordedit)
    return newlist

#Handles a paragraph of text and returns a tuplelist of better organized sentences
def handleText(tuplelist, minlength):
    tuplelist = sentenceConverter(tuplelist)
    tuplelist = smallSentenceFilter(tuplelist, minlength)
    tuplelist = textCleanup(tuplelist)
    return tuplelist
