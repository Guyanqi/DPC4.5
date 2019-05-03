from optparse import OptionParser
import logging
import config
import sys
import RandomForest
import DecisionTree
from util import ResultParser
from util import DataLoader


def main():

    parser = OptionParser()
    parser.add_option("-i", dest="inc", default='dataset', help="dataset directory")
    parser.add_option("-f", "--file", dest="fileName", default='car', help="file name of training dataset")
    parser.add_option("-c", "--class-attr", dest="classAttr", default='class', help="classification attribute")
    parser.add_option("-d", "--depth", dest="depth", default=6, help="max recursion depth of decision trees")
    parser.add_option("-t", "--tree-num", dest="treeNum", default=10, help="num of decision trees")
    parser.add_option("-e", "--epsilon", dest="epsilon", default=1, help="total privacy budget")
    parser.add_option("-v", "--verbose", dest="verbose", default=True, help="open verbose mode")
    parser.add_option("--mode", dest='mode', default='All', help='choose build mode: DecisionTree/RandomForest/ALL')
    (options, args) = parser.parse_args()

    if options.verbose:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logging.info('Init Decision Tree to build data')
    trainFileName = options.inc + '/' + options.fileName + 'Training.csv'
    testFileName = options.inc + '/' + options.fileName + '.csv'
    
    dataRaw = DataLoader.getData(trainFileName)
    attributes = dataRaw[0]
    attributesType = dataRaw[1]
    if logging.DEBUG:
        for index in range(0, len(attributesType)):
            logging.debug('attr: %s; attrType: %s', attributes[index], attributesType[index])
            logging.debug('class attr: %s', attributes[-1])

    dataRaw.remove(attributes)
    dataRaw.remove(attributesType)
    dataTrain = DataLoader.toFloat(dataRaw, attributesType)

    dataTestRaw = DataLoader.getData(testFileName)
    dataTest = DataLoader.toFloat(dataTestRaw, attributesType)
    classStd = []
    for row in dataTest:
        classStd.append(row[-1])

    target = options.classAttr
    depth = options.depth
    treeNum = options.treeNum
    epsilon = options.epsilon
    logging.debug('target: %s', target)
    logging.debug('depth: %s', str(depth))

    if config.config.MakeTree == 'DecisionTree' or config.config.MakeTree == 'All':

        # Run C4.5
        logging.info('Run C4.5 to generate Decision Tree')
        tree = DecisionTree.makeTree(dataTrain, attributes, attributesType, target, depth, depth, epsilon)
        # Classify testing data
        logging.debug('Classify testing data by generated Decision Tree')
        classResult = DecisionTree.classify(tree, attributes, attributesType, dataTest)
        # Output Classification Accuracy
        acc = ResultParser.classAccDecisionTree(classStd, classResult)
        logging.info('Classification Accuracy: ' + str(acc))

    if config.config.MakeTree == 'RandomForest' or config.config.MakeTree == 'All':

        # Run Random Forest
        logging.info('Run RandomForest to generate Decision Tree')
        trees = RandomForest.randomForest(dataTrain, attributes, attributesType, target, depth, depth, treeNum, epsilon)
        classResults = []
        for tree in trees:
            classResult = DecisionTree.classify(tree, attributes, attributesType, dataTest)
            classResults.append(classResult)
        acc = ResultParser.classAccRandomForest(classStd, classResults)
        logging.info('Classification Accuracy: ' + str(acc))


if __name__ == '__main__':
    main()
