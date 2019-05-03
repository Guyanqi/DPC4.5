def classAccDecisionTree(classStd, classRes):
    count = 0;
    for idx in range(len(classRes)):
        if classStd[idx] == classRes[idx]:
            # logging.debug('Result Incorrect %d: %s!=%s', count, class0[idx], class1[idx])
            count += 1

    res = 1.000*count/len(classStd)
    
    return res


def majority(classResults):
    classResult = []
    if len(classResults[0]) == 0:
        return classResults
    for idxRequery in range(0, len(classResults[0])):
        valFreq = {}
        for result in classResults:
            if result[idxRequery] in valFreq:
                valFreq[result[idxRequery]] += 1
            else:
                valFreq[result[idxRequery]] = 1
        max = 0
        val = ''
        for key in valFreq.keys():
            if valFreq[key] > max:
                max = valFreq[key]
                val = key
        classResult.append(val)
    return classResult


def classAccRandomForest(classStd, classResults):
    classResult = majority(classResults)
    return classAccDecisionTree(classStd, classResult)

