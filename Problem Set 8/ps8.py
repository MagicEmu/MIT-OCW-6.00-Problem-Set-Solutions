# 6.00 Problem Set 8
#
# Intelligent Course Advisor
#
# Name: Yichen Dai
# Collaborators:
# Time:
#

import time

SUBJECT_FILENAME = "subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    inputFile = open(filename)
    subjects = {}
    for line in inputFile:
        line.strip()
        course = line.split(',')
        subjects[course[0]] = (int(course[1]), int(course[2]))
    return subjects
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course  Value  Work\n======  =====  ====\n'
    subNames = subjects.keys()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '   ' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value: ' + str(totalVal) +'\n'
    res = res + 'Total Work: ' + str(totalWork) + '\n'
    print(res)

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    return  val1 > val2

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return  work1 < work2

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    val1 = subInfo1[VALUE]
    val2 = subInfo2[VALUE]
    work1 = subInfo1[WORK]
    work2 = subInfo2[WORK]
    return float(val1) / work1 > float(val2) / work2

#
# Problem 2: Subject Selection By Greedy Optimization
#
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    workload = 0
    selected = {}
    temp = subjects.copy()
    while workload < maxWork:
        subNames = list(temp.keys())
        best = subNames[0]
        for i in range(len(subNames)-1):
            if comparator(temp[subNames[i+1]], temp[best]):
                best = subNames[i+1]
        if workload + temp[best][WORK] > maxWork:
            break
        else:
            workload += temp[best][WORK]
            selected[best] = temp[best]
        del(temp[best])
    return selected

def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    nameList = list(subjects.keys())
    tupleList = list(subjects.values())
    bestSubset, bestSubsetValue = \
            bruteForceAdvisorHelper(tupleList, maxWork, 0, None, None, [], 0, 0)
    outputSubjects = {}
    for i in bestSubset:
        outputSubjects[nameList[i]] = tupleList[i]
    return outputSubjects

def bruteForceAdvisorHelper(subjects, maxWork, i, bestSubset, bestSubsetValue,
                            subset, subsetValue, subsetWork):
    # Hit the end of the list.
    if i >= len(subjects):
        if bestSubset == None or subsetValue > bestSubsetValue:
            # Found a new best.
            return subset[:], subsetValue
        else:
            # Keep the current best.
            return bestSubset, bestSubsetValue
    else:
        s = subjects[i]
        # Try including subjects[i] in the current working subset.
        if subsetWork + s[WORK] <= maxWork:
            subset.append(i)
            bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                    maxWork, i+1, bestSubset, bestSubsetValue, subset,
                    subsetValue + s[VALUE], subsetWork + s[WORK])
            subset.pop()
        bestSubset, bestSubsetValue = bruteForceAdvisorHelper(subjects,
                maxWork, i+1, bestSubset, bestSubsetValue, subset,
                subsetValue, subsetWork)
        return bestSubset, bestSubsetValue

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceTime():
    """
    Runs tests on bruteForceAdvisor and measures the time required to compute
    an answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    for i in range(8):
        startTime = time.time()
        bruteForceAdvisor(subjects, i)
        endTime = time.time()
        totalTime = endTime - startTime
        print('the maximum workload of', i, 'hours takes', totalTime, 'seconds to compute with brute force')

# Problem 3 Observations
# ======================
#
# Each extra hour of workload takes the program substantially longer to compute
# the time about triples with each extra work hour
# 1 hour takes only a hundredth of a second, while 10 hours takes over 2 minutes
# program is exponential as for each time n increases, it multiplies by 3

#
# Problem 4: Subject Selection By Dynamic Programming
#
def dpAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work) that contains a
    set of subjects that provides the maximum value without exceeding maxWork.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    courses = tuple(subjects.keys())
    temp = [[[0, ()] for x in range(maxWork + 1)] for x in range(len(courses) + 1)]
    for i in range(len(courses)+1):
        for w in range(maxWork+1):
            if w == 0 or i == 0:
                temp[i][w][0] = 0
            elif subjects[courses[i-1]][WORK] <= w:
                if subjects[courses[i-1]][VALUE] + temp[i - 1][w - subjects[courses[i-1]][WORK]][0] > temp[i-1][w][0]:
                    temp[i][w][0] = subjects[courses[i-1]][VALUE] + temp[i - 1][w - subjects[courses[i-1]][WORK]][0]
                    temp[i][w][1] = temp[i - 1][w - subjects[courses[i-1]][WORK]][1] + (courses[i-1],)
                else:
                    temp[i][w][0] = temp[i - 1][w][0]
                    temp[i][w][1] = temp[i - 1][w][1]
            else:
                temp[i][w][0] = temp[i-1][w][0]
                temp[i][w][1] = temp[i-1][w][1]
    selected = {}
    for course in temp[len(courses)][maxWork][1]:
        selected[course] = subjects[course]
    return selected

#
# Problem 5: Performance Comparison
#
def dpTime():
    """
    Runs tests on dpAdvisor and measures the time required to compute an
    answer.
    """
    subjects = loadSubjects(SUBJECT_FILENAME)
    for i in range(8):
        startTime = time.time()
        res = dpAdvisor(subjects, i)
        endTime = time.time()
        totalTime = endTime - startTime
        print('the maximum workload of', i, 'hours takes', totalTime, 'seconds to compute with dynamic programming')

printSubjects(dpAdvisor(loadSubjects(SUBJECT_FILENAME), 27))

# Problem 5 Observations
# ======================
#
# dpAdvisor is very quick, takes less than a second and increases at a constant of 0.002 seconds for
# each extra hour. (linear)
# brute force is slower, the time it takes triples for each extra hour (exponential)
