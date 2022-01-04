from string import *

def countSubStringMatch(target, key):
    count = 0
    i=target.find(key)
    while i<len(target):
        if i == -1:
            break
        count += 1
        i = target.find(key, i+1)
    return count

def countSubStringMatchRecursive(target, key, count):
    if len(target) == 0:
        return count
    if target.find(key) != -1:
        count += 1
    index = target.find(key)
    return countSubStringMatchRecursive(target[index:], key, count)

def subStringMatchExact(target, key, matches):
    if len(target) == 0:
        return matches
    if target.find(key) != -1:
        matches += [target.find(key)+len(matches)]
    elif target.find(key) == -1:
        return matches
    index = target.find(key)+len(key)
    return subStringMatchExact(target[index:], key, matches)

def constrainedMatchPair(firstMatch, secondMatch, length, i, matches):
    if i == len(firstMatch):
        return matches
    for j in secondMatch:
        if j == firstMatch[i] + length + 1:
            matches += [i]
    return constrainedMatchPair(firstMatch, secondMatch, length, i+1, matches)

def subStringMatchExactlyOneSub(target,key, matches):
    found = False
    index = 0
    for i in range(len(key)):
        if target.find(key[:i]) != -1 and target.find(key[i + 1:]) != -1 and target.find(key[:i]) == target.find(key[i+1:])-1:
            matches += [target.find(key[:i])]
            index = target.find(key[:i]) + len(key)
            found = True
            break
    if found == False:
        return matches
    return subStringMatchExactlyOneSub(target[index:],key, matches)

subStringMatchExactlyOneSub('aaaa','ab', [])