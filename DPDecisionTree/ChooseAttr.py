import random
import config

# choose the attribute with the highest value
def chooseAttrByMaxValue(attrsInfo):
    typeName = config.config.ChooseBestAttrTypeName
    maxGain = 0.0
    best = {
        typeName: maxGain,
        'attr': attrsInfo.keys()[0]
    }

    for attr in attrsInfo.keys():
        if attrsInfo[attr][typeName] > maxGain:
            maxGain = attrsInfo[attr][typeName]
            best['attr'] = attr
            best[typeName] = maxGain
            if 'splitPoint' in attrsInfo[attr]:
                best['splitPoint']=attrsInfo[attr]['splitPoint']
    return best


# choose the attribute according to the probability
def chooseAttrByProbability(attrsInfo):
    typeName = config.config.ChooseBestAttrTypeName
    probs = []
    sum = 0
    for attr in attrsInfo.keys():

        prob = round(attrsInfo[attr]['probability'] * 1000000000)
        attrsInfo[attr]['probability'] = prob
        sum = sum + prob
    rand = random.randint(1, sum)
    for attr in attrsInfo.keys():
        if rand <= attrsInfo[attr]['probability']:
            best = {}
            best['attr'] = attr
            best[typeName] = attrsInfo[attr][typeName]
            if 'splitPoint' in attrsInfo[attr]:
                best['splitPoint'] = attrsInfo[attr]['splitPoint']
            return best
        else:
            rand = rand - attrsInfo[attr]['probability']


# choose best attribute
def chooseAttr(data, attributes, attributesType, target, epsilon = 0):

    #chooseFunc can be InfoGain or MaxOperator
    #typeName can be entropy or maxOPerator(this is attrsInfo[attr][typeName] key)
    #DifferentialPrivacyFunc = ExponentialMechanism.exponentialMechanism or NULL
    #scoreFuncSensitivity represents the score function's sensitivity(1 or log2(|class|))
    chooseFunc = config.config.ChooseBestAttr
    typeName = config.config.ChooseBestAttrTypeName
    differentialPrivacyFunc = config.config.DifferentialPrivacyFunc
    scoreFuncSensitivity = config.config.ScoreFuncSensitivity

    #attrsInfo [attr]['probability']
    #                ['splitPoint'](if the attr is numerical)
    #                [typeName](infoGain or maxOperator)
    attrsInfo = {}
    for attr in attributes:
        if attr != target:
            #each attr's score
            newAttrInfo =  chooseFunc(data, attributes, attributesType, attr, target)
            attrsInfo[attr] = {}
            attrsInfo[attr][typeName] = newAttrInfo[typeName]
            #if exponentialMechanism calculate attr's prob
            if not differentialPrivacyFunc is None:
                prob = differentialPrivacyFunc(newAttrInfo[typeName], scoreFuncSensitivity, epsilon)
                attrsInfo[attr]['probability'] = prob
            index = attributes.index(attr)
            type = attributesType[index]
            if (type == 'Numerical'):
                attrsInfo[attr]['splitPoint'] = newAttrInfo['splitPoint']

    best = {}
    # according to the differentialPrivacyFunc, choose the best attr
    if differentialPrivacyFunc is None:
        best = chooseAttrByMaxValue(attrsInfo)
    else:
        best = chooseAttrByProbability(attrsInfo)

    # if a numerical attr can't split any more, give it a key continueSplit, so that it becomes a leaf
    if best[typeName] == 0:
        best['continueSplit'] = 1

    return best


