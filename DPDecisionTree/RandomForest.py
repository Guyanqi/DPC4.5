import DecisionTree
import random
import math


def randomForest(data, attributes, attributesType, target, depth, recursion, treeNum, epsilon=0):
    # generate a random number
    # choose attr and data
    # generate trees
    trees = []
    attrNum = math.sqrt(len(attributes))
    epsilonPerTree = float(epsilon)/treeNum
    for i in range(0, treeNum):
        newData = genDataset(data)
        attrAndType = genAttrbutes(attributes, attributesType, attrNum, target)
        newAttributes = attrAndType['attr']
        newAttrTypes = attrAndType['type']
        newDataset = genNewDataset(newData, newAttributes, attributes)
        tree = DecisionTree.makeTree(newDataset, newAttributes, newAttrTypes, target, depth, recursion, epsilonPerTree)
        trees.append(tree)
    return trees


def genDataset(data):
    newData = []
    for i in range(0,len(data)):
        index = random.randint(0,len(data)-1)
        newData.append(data[index])
    return newData


# modify same attr and the classAttr should be the last attr
def genAttrbutes(attributes, attributesType, attrNum, target):
    choosenAttr = []
    choosenAttrType = []
    ret = {}
    while len(choosenAttr) < attrNum:
        index = random.randint(0, len(attributes)-2)
        if attributes[index] not in choosenAttr:
            choosenAttr.append(attributes[index])
            choosenAttrType.append(attributesType[index])
    choosenAttr.append(attributes[-1])
    ret['attr'] = choosenAttr
    ret['type'] = choosenAttrType
    return ret


def genNewDataset(data, newAttr, attributes):
    newData = []
    for entry in data:
        newEntry = []
        for attr in newAttr:
            index = attributes.index(attr)
            newEntry.append(entry[index])
        newData.append(newEntry)
    return newData