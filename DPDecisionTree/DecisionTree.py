import sys
sys.path.append("..")
import logging
import ChooseAttr
from DPDecisionTree.lib import ExponentialMechanism
from DPDecisionTree.lib import LaplaceMechanism


# find most common value for an attribute
def majority(attributes, data, target, epsilon=0):
    valFreq = {}
    # find target in data
    index = attributes.index(target)
    # count frequency of value in target attr
    for tuple in data:
        if tuple[index] in valFreq:
            valFreq[tuple[index]] += 1 
        else:
            valFreq[tuple[index]] = 1
    max = 0
    major = ""                                                                                                                                                               
    for key in valFreq.keys():
        if epsilon != 0:
            valFreq[key] = LaplaceMechanism.laplaceMechanism(valFreq[key], epsilon)
        if valFreq[key] > max:
            max = valFreq[key]
            major = key
    return major


# get values in the column of the given attribute
def getValues(data, attributes, attr):
    index = attributes.index(attr)
    values = []
    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])
    return values


# get the subset data for numerical attribute which 
# will divide current data into two parts by splitPoint
def getSubDataNum(data, attributes, attr, splitPoint):
    index = attributes.index(attr)
    subDataLower = []
    subDataHigher = []
    for entry in data:
        if entry[index] < splitPoint:
            subDataLower.append(entry)
        elif entry[index] > splitPoint:
            subDataHigher.append(entry)

    return [subDataLower, subDataHigher]


# get the subset data for categorical attribute which 
# will divide current data into multiple parts by val
def getSubDataCat(data, attributes, best, val):
    examples = [[]]
    index = attributes.index(best)
    for entry in data:
        # find entries with the give value
        if (entry[index] == val):
            newEntry = []
            # add value if it is not in best column
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            examples.append(newEntry)
    examples.remove([])
    return examples


def makeTree(data, attributes, attributesType, target, depth, recursion, epsilon=0):
    epsilonPerLevel = epsilon / (2.0 * (depth + 1))
    recursion -= 1
    vals = [record[attributes.index(target)] for record in data]
    default = majority(attributes, data, target, epsilonPerLevel)

    # If data set is empty throw error
    if not data:
        logging.fatal('ERROR: data is empty')

    # If attributes list is empty or recursion reachs depth option 
    # return default 
    elif (len(attributes) - 1) <= 0 or recursion <= 0:
        return {'leaf': default}

    # If all the records in the dataset have the same classification,
    # return that classification.
    elif vals.count(vals[0]) == len(vals):
        return {'leaf': vals[0]}

    # build the decision tree recursively
    else:
        # Choose the next best attribute to best classify our data
        best = ChooseAttr.chooseAttr(data, attributes, attributesType, target, epsilonPerLevel)
        logging.debug('Split Attr: %s', best['attr'])

        if 'continueSplit' in best:
            return {'leaf': default}
        bestAttr = best['attr']
        index = attributes.index(bestAttr)
        type = attributesType[index]

        if type == 'Categorical':
            # Create a new decision tree/node with the best attribute and an empty
            tree = {'attr': bestAttr, 'subTree': {}}
        
            # Create a new decision tree/sub-node for each of the values in the
            # best attribute field
            for val in getValues(data, attributes, bestAttr):
                # Create a subtree for the current value under the "best" field
                subData = getSubDataCat(data, attributes, bestAttr, val)
                newAttributes = attributes[:]
                newAttributes.pop(index)
                newAttributesType = attributesType[:]
                newAttributesType.pop(index)
                subtree = makeTree(subData, newAttributes, newAttributesType, target, depth, recursion)
        
                # Add the new subtree to the empty dictionary object in our new
                # tree/node we just created.
                tree['subTree'][val] = subtree
    
        elif type == 'Numerical':
            # add the tree node with 'attr', 'splitPoint' and 'subTree'
            # build up two subTrees recursively which is divided by splitPoint
            splitPoint = best['splitPoint']
            tree = {'attr': bestAttr, 'splitPoint': splitPoint, 'subTree': {}}

            # get two subset Data
            [subDataLower, subDataHigher] = getSubDataNum(data, attributes, bestAttr, splitPoint)
            # get two subTree
            subTreeLower = makeTree(subDataLower, attributes, attributesType, target, depth, recursion)
            subTreeHigher = makeTree(subDataHigher, attributes, attributesType, target, depth, recursion)
            # construct current tree node
            tree['subTree']['lower'] = subTreeLower
            tree['subTree']['higher'] = subTreeHigher
    
    return tree


# according our decision tree, put each record in dataset into a leaf
def classify(tree, attributes, attributesType, query):
    res = []
    for entry in query:
        tmpTree = tree.copy()
        result = ''
        # traverse the tree until reach leaf node
        while ('leaf' not in tmpTree):
            attr = tmpTree['attr']
            index = attributes.index(attr)
            type = attributesType[index]
            value = entry[index]

            if type == 'Categorical':
                if value in tmpTree['subTree'].keys():
                    tmpTree = tmpTree['subTree'][value]
                else:
                    # in Categorical attribute if a value is not 
                    # presented in training set then treat it as
                    # an unknow class and return question mark
                    result = '?'
                    break
            elif type == 'Numerical':
                if value <= tmpTree['splitPoint']:
                    tmpTree = tmpTree['subTree']['lower']
                else:
                    tmpTree = tmpTree['subTree']['higher']
            else:
                print('ERROR attribute type')
                exit(1)

        if result != '?':
            result = tmpTree['leaf']
        res.append(result)
    return res
