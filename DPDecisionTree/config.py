from lib import InfoGain
from lib import MaxOperator
from lib import ExponentialMechanism
from inc import naming


class Config:
    name = 'Global Configuration'
    printMe = 'Config File'
    MakeTree = 'All'

    # 0: info gain
    # 1: max operator

    ChooseBestAttrMethodGroupNumber = 1
    ChooseBestAttr = None
    ChooseBestAttrTypeName = ''
    # the way to choose the best attr to as split attr in next build tree cycle
    # change 'ChooseBestAttr' and 'ChooseBestAttrTypeName' together
    # (InfoGain.gain, MaxOperator.maxOperator)
    # 'ChooseBestAttr': InfoGain.gain,MaxOperator.maxOperator
    # 'ChooseBestAttrTypeName': naming.ENTROPY_NAME, naming.MAXOPERATOR_NAME
    # 0: use basic choose method
    # 1: use exponential mechanism to choose attribute
    DifferentialPrivacyFuncNumber = 1
    DifferentialPrivacyFunc = None
    # 'DifferentialPrivacyFunc': ExponentialMechanism.exponentialMechanism
    ScoreFuncSensitivity = 1

    def __init__(self):
        # Info Gain
        if self.ChooseBestAttrMethodGroupNumber == 0:
            self.ChooseBestAttr = InfoGain.gain
            self.ChooseBestAttrTypeName = naming.ENTROPY_NAME

        # Max Operator
        elif self.ChooseBestAttrMethodGroupNumber == 1:
            self.ChooseBestAttr = MaxOperator.maxOperator
            self.ChooseBestAttrTypeName = naming.MAXOPERATOR_NAME

        if self.DifferentialPrivacyFuncNumber == 0:
            self.DifferentialPrivacyFunc = None
        elif self.DifferentialPrivacyFuncNumber == 1:
            self.DifferentialPrivacyFunc = ExponentialMechanism.exponentialMechanism


config = Config()

