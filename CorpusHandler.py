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
