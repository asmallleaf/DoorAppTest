from app_2_0_0.app.support.verifySupportTool import VerifySupportToolFactory as VSF
from app_2_0_0.app.support.dbSupportTool import dbSupportToolFactory as DBSF
from enum import Enum

class supportNames(Enum):
    verify = 0
    database = 1

class Supports():

    @classmethod
    def create(cls,name):
        if name == supportNames['verify']:
            return VSF.build()
        elif name == supportNames['database']:
            return DBSF.build()

    @classmethod
    def createBundle(cls,args):
        for arg in args:
            return cls.create(arg)

