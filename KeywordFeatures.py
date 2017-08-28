import re

parallels = ['first', 'second', 'third', 'fourth', 'fifth', 'firstly', 'secondly', 'thirdly', 'fourthly', 'fifthly', 'next', 'then', 'finally', 'last', 'lastly','for one thing', 'to begin with', 'to conclude', 'above all', 'on top of it all', 'and what is more', 'first of all', 'ultimately']
inferentials = ['as a result', 'because of this', 'therefore','consequently','hence', 'as a consequence', 'if so', 'if not', 'that implies', 'i deduce from that', 'you can conclude from that', 'it follows that', 'thereby', 'thus']
details = ['for instance','in particular','another instance is']
summaries = ['to conclude', 'to summarize', 'in sum', 'altogether', 'overall', 'all in all', 'in conclusion','to conclude', 'to summarize', 'i will sum by saying', 'my conclusion is', 'summarizing', 'to sum up']
reformulations = ['in other words', 'in short', 'that is to say', 'namely', 'that is', 'alternately', 'put another way']
contrasts = ['although', 'but', 'conversely', 'on the contrary', 'in contrast', 'by comparison', 'nonetheless', 'though','in any case', 'at any rate', 'after all', 'in spite of that', 'meanwhile', 'rather than', 'i would rather say', 'the alternative is', 'despite', 'alternatively', 'by contrast', 'on the other hand', 'nevertheless', 'on the one side', 'still']
conjunctions = ['and', 'in addition', 'furthermore', 'additionally','in fact', 'moreover', 'separately', 'equally', 'likewise', 'similarly', 'too', 'in a similar vein', 'not only', 'indeed', 'nor']

def testStart(wordlist, word):
    try:
        ind= wordlist.index(word)
        if ind<3:
            return True
        return False
    except:
        return False
                
def containsKeyword(sent):
    count=0
    for word in parallels:
        if word in sent:
            if testStart(sent, word):               
                count+=0
    for word in inferentials:
        if word in sent:
            count+=1
    for word in details:
        if word in sent:
            count+=1
    for word in summaries:
        if word in sent:
            count+=1
    for word in reformulations:
        if word in sent:
            count+=0
    for word in contrasts:
        if word in sent:
            count+=1
    for word in conjunctions:
        if word in sent:
            count+=0
    if 'either' in sent:
        if 'or' in sent:
            count+=1
    return count

def parWord(editsent, nltksent):
    for word in parallels:
        split = word.split(' ')
        if word in editsent and len(split)>1:
            return word
        else:
            for word2, tag in nltksent:
                if word==word2 and tag=='RB':
                    return word
    return ''
def infWord(editsent, nltksent):
    for word in inferentials:
        split = word.split(' ')
        if word in editsent and len(split)>1:
            return word
        else:
            for word2, tag in nltksent:
                if word==word2:
                    return word
    return ''
def detWord(editsent):
    for word in details:
        if word in editsent:
            return word
    return ''
def sumWord(editsent, nltksent):
    for word in summaries:
        split = word.split(' ')
        if word in editsent and len(split)>1:
            return word
        else:
            for word2, tag in nltksent:
                if word==word2 and tag=='RB':
                    return word
    return ''
def refWord(editsent):
    for word in reformulations:
        if word in editsent:
            return word
    return ''
def contWord(editsent, nltksent):
    for word in contrasts:
        split = word.split(' ')
        if word in editsent and len(split)>1:
            return word
        else:
            for word2, tag in nltksent:
                if word==word2 and tag=='RB':
                    return word
    return ''

def conjWord(editsent, nltksent):
    for word in conjunctions:
        split = word.split(' ')
        if word in editsent and len(split)>1:
            return word
        else:
            for word2, tag in nltksent:
                if word==word2:
                    return word
    return ''

