import logging


# modify the numerical input to float, and delete the '?'
def toFloat(data, attributesType):
    ret = []
    for entry in data:
        newEntry = []
        invalidEntry = False
        for index in range(0, len(entry)-1):
            if entry[index] == '?':
                invalidEntry = True
            elif attributesType[index] == 'Numerical':
                try:
                    newEntry.append(float(entry[index]))
                except ValueError:
                    logging.warning('Invalid attribute: %s', entry[index])
                    invalidEntry = True
            else:
                newEntry.append(entry[index])
        if invalidEntry:
            logging.warning("Invalid entry in data %s", entry)
        else:
            newEntry.append(entry[-1])
            ret.append(newEntry)
    return ret


# attributes' num == attributesType's num
def attrValidation(data, attributes, attributesType):
    return 1


# data's attr's num
def dataValidation(data, attributes):
        return 1


def getData(fileName):
    logging.info('fetch data from file: ' + fileName)
    file = open(fileName)
    data = []
    for line in file:
        line = line.strip("\r\n")
        data.append(line.split(','))
    return data
