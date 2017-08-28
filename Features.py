import nltk
import KeywordFeatures as kf

def TCsFeatures(sent, count, arglist, secondtime=False, person=''):
    editsent=''
    for letter in sent:
        letter=letter.lower()
        if letter.isalnum() or letter == ' ': 
            editsent+=letter
    splitsent = nltk.tokenize.word_tokenize(sent)
    nltksent = nltk.pos_tag(splitsent)
    keywamt = kf.containsKeyword(editsent)
    modal = modalVerb(nltksent)
    because = containsBecause(nltksent)
    tup=arglist[count]
    firstpers = fp(splitsent)
    stance= addStanceExp(nltksent)
    question = questionSent(sent)
    pt = PTVerb(nltksent)
    belief = beliefWord(editsent)
    parword = kf.parWord(editsent, nltksent)
    infword = kf.infWord(editsent, nltksent)
    detword = kf.detWord(editsent)
    sumword = kf.sumWord(editsent, nltksent)
    refword = kf.refWord(editsent)
    contword = kf.contWord(editsent, nltksent)
    firstnoun = noun(nltksent)
    firstverb = verb(nltksent)
    interrupted = interruptSent(splitsent)
    ip = interpunctCount(nltksent)
    if secondtime==True:
        extfeats = extendedFeaturesv2(count, arglist)
    else:
        extfeats = extendedFeaturesv1(count, arglist)  
    features ={'interr':interrupted,'ref':refword, 'nn':belief,'cc':cc(nltksent),'in':In(nltksent),'jjs':jjs(nltksent),'cont':contword, \
               'so':containsSo(nltksent),'compareavb': comparativeAdverb(nltksent), \
               'to':to(nltksent),'length':len(sent),'modalverb': modal,'verb':firstverb, 'sentence':sent, 'keywamt':keywamt,\
               'containsbecause':because, '?sent':questionSent(sent), 'fp':firstpers}
    features.update(extfeats)
    return features
def jjs(nltksent):
    for word, tag in nltksent:
        if tag=='JJS':
            return word
    return ''

def In(nltksent):
    notlist=['if', 'by', 'as', 'about']
    for word, tag in nltksent:
        if tag=='IN' and word not in notlist:
            return word
    return ''

def cc(nltksent):
    notlist=['but', 'and', 'or']
    for word, tag in nltksent:
        if tag=='CC' and word not in notlist:
            return word
    return ''
"""These features extend the standard feature list by adding features that are based on the
position of the sentence within the text."""
def extendedFeaturesv1(count, arglist):
    features = {}
    prevsent = prevSentType(count, arglist)
    spprevsent = samePersPrevSentType(count, arglist)
    spprev = prevSentSamePers(count, arglist)
    features.update(prevsent)
    features.update(spprevsent)
    return features

def extendedFeaturesv2(count, arglist):
    features = {}
    prevsent = prevSentType(count, arglist)
    spprev = prevSentSamePers(count, arglist)
    spprevsent = samePersPrevSentType(count, arglist)
    nextsent = nextSentType(count, arglist)
    spnext = nextSentSamePers(count, arglist)
    spnextsent = samePersNextSentType(count, arglist)
    features.update(prevsent)
    features.update(spprevsent)
    features.update(spnextsent)
    return features

def comparativeAdverb(nltksent):
    for word, tag in nltksent:
        if tag == 'RBS' or tag=='RBR':
            return word
    return '' 

def to(nltksent):
    for word, tag in nltksent:
        if tag == 'TO':
            return word
    return ''    
def containsSo(nltksent):
    for word, tag in nltksent:
        if word == 'so':
            return word
    return '' 
"""Returns a feature containing the type (Reg, Claim or Premise) of the previous sentence spoken
by the same person"""
def samePersPrevSentType(count, arglist):
    tup = arglist[count]
    person = tup[0]
    while count>0:
        count-=1
        prevtup= arglist[count]
        person2 = prevtup[0]
        if person2==person:
            return {'prevsenttypesp':prevtup[1]}
    return {'prevsenttypesp':'None'}

def prevSentType(count, arglist):
    if count>0:
        tup = arglist[count-1]
        return {'prevsenttype':tup[1]}
    else:
        return {'prevsenttype':'None'}

def prevSentSamePers(count, arglist):
    tup = arglist[count]
    person = tup[0]
    if count>0:
        prevtup = arglist[count-1]
        person2 = prevtup[0]
        if person2==person:
            return {'prevsentsp':True}
    return {'prevsentsp':False}

def nextSentSamePers(count, arglist):
    tup = arglist[count]
    person = tup[0]
    if count<len(arglist)-1:
        prevtup = arglist[count+1]
        person2 = prevtup[0]
        if person2==person:
            return {'nextsentsp':True}
    return {'nextsentsp':False}

def samePersNextSentType(count, arglist):
    tup = arglist[count]
    person = tup[0]
    while count<len(arglist)-1:
        count+=1
        nexttup= arglist[count]
        person2 = nexttup[0]
        if person2 == person:
            return {'nextsenttypesp':nexttup[1]}
    return {'nextsenttypesp':'None'}

def nextSentType(count, arglist):
    if count<len(arglist)-1:
        tup = arglist[count+1]
        return {'nextsenttype':tup[1]}
    else:
        return {'nextsenttype':'None'}

def questionSent(sent):
    for letter in sent:
        if letter =='?':
            return True
    return False

def noun(nltksent):
    for word, tag in nltksent:
        if tag == 'NN' or tag == 'NNS':
            return word
    return ''

def verb(nltksent):
    for word, tag in nltksent:
        if tag[0]=='V':
            return word
    return ''

def containsBecause(nltksent):
    for word, tag in nltksent:
        if word=='because':
            return True
    return False

def interruptSent(splitsentence):
    for word in splitsentence:
        for letter in word:
            if letter == '-':
                return True
    return False

def modalVerb(nltksent):
    for word, tag in nltksent:
        if tag == 'MD':
            return word
    return ''

def beliefWord(editsent):
    count = 0
    beliefwords = ['primarily', 'principally', 'especially', 'chiefly', 'largely', 'mainly', 'mostly', 'notably', 'certainly','definitely', 'indeed', 'plainly', 'really','surely','for sure', 'frankly', 'honestly', 'literally','kind of', 'sort of',  'mildly', 'moderately', 'partially', 'slightly', 'somewhat', 'in part', 'in some respects', 'to some extent', 'scarcely', 'hardly', 'barely,' 'a bit',  'in the least', 'in the slightest', 'almost', 'nearly', 'virtually', 'practically', 'approximately', 'briefly', 'broadly', 'roughly', 'admittedly', 'decidedly', 'definitely', 'doubtless', 'reportedly', 'amazingly', 'remarkably', 'naturally', 'fortunately', 'tragically', 'unfortunately', 'delightfully', 'annoyingly', 'thankfully','justly']
    for word in beliefwords:
        if word in editsent:
            return word
    return ''

def fp(splitsentence):
    count=0
    fpwords = ['i', 'me', 'my', 'mine', 'myself']
    for word in splitsentence:
        if word in fpwords:
            return True
    return False

def longWordCount(splitsentence):
    threshold = 10
    count = 0
    for word in splitsentence:
        if len(word)>=threshold:
            return True
    return False
    
def PTVerb(nltksentence):
    count = 0
    for word, tag in nltksentence:
        if tag=='VBD':
            return True
    return False

def addStanceExp(nltksentence):
    count=0
    stancelist=['believe','believe','think','find','suggest','recommend','like']
    for word, tag in nltksentence:
        if tag[0]=='V' and word in stancelist:
            return word
    return ''


def interpunctCount(nltksent):
    count = 0
    for word, tag in nltksent:
        if word.isalnum() == False:
            count+=1
    return count




def StabFeatures(sent, prevarg):
    editsent=''
    for letter in sent:
        letter=letter.lower()
        if letter.isalnum() or letter == ' ': 
            editsent+=letter
    splitsent = nltk.tokenize.word_tokenize(sent)
    nltksent = nltk.pos_tag(splitsent)
    keywamt = kf.containsKeyword(editsent)
    amtpar=kf.amtpar(editsent)
    amtinf=kf.amtinf(editsent)
    amtdet=kf.amtdet(editsent)
    amtsum=kf.amtsum(editsent)
    amtref=kf.amtref(editsent)
    amtcont=kf.contWord(editsent)
    prevtag = prevTag(prevarg)
    modalamt = modalVerbAmt(splitsent)
    beliefamt = beliefWordAmt(splitsent)
    fpcount = firstPersonCount(splitsent)
    lwcount = longWordCount(splitsent)
    amtPT = PTVerbCount(nltksent)
    stanceamt= addStanceExpCount(nltksent)
    ipcount = interpunctCount(nltksent)
    return {'parkey':amtpar,'infkey':amtinf,'detkey':amtdet,'sumkey':amtsum,'refkey':amtref, 'fp':fpcount, 'contkey':amtcont,'keysamt':keywamt,'hasmodal': modalamt, 'hasbelief':beliefamt, 'haslw': lwcount,'hasstance':stanceamt, 'ipcount':ipcount} 
