import nltk
import collections
import Features

def TCsArgTraining(arglist):
    featureset = featureSet(arglist)
    trainsents = featureset
    classifier= nltk.NaiveBayesClassifier.train(trainsents)
    return classifier

def featureSet(arglist):
    featureset = []
    c=0
    while c<len(arglist):
        tup = arglist[c]
        tag = tup[1]
        featureset.append((Features.TCsFeatures(tup[2], c, arglist, True), tag))
        c+=1
    return featureset














