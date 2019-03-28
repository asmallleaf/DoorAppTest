from app_2_0_0.app.verify.userVerify import UserVerifyFactory
from app_2_0_0.app.verify.homeVerify import HomeVerifyFactory
from app_2_0_0.app.toolbox.basetool import SupportToolFactory,SupportTool
from app_2_0_0.app.config.config import Test_Config
from app_2_0_0.app.toolbox.iotool import IOtool
from enum import Enum

class Type(Enum):
    user = 0
    home = 1

class VerifySupportToolFactory(SupportToolFactory):
    def build(self):
        return VerifySupportTool()

class VerifySupportTool(SupportTool):
    def __init__(self):
        self.verify = UserVerifyFactory().build()
        self.home = HomeVerifyFactory.build()
        self.request = None
        self.dbSupport = None
        self.token = None
        self.name = None
        self.KEY = Test_Config().TOKEN

    def setDbSupport(self,value):
        self.dbSupport = value
        return self

    def setRequest(self,value):
        self.request = value
        return self

    def getError(self,type):
        if type == Type.user:
            return self.verify.getError()
        elif type == Type.home:
            return self.home.getError()

    def getSuccess(self,type):
        if type == Type.user:
            return self.verify.getSuccess()
        elif type == Type.home:
            return self.home.getSuccess()

    def verifyLogin(self):
        name = None
        password = None
        if self.request.method == 'POST':
            name = self.request.form.get('userName')
            password = self.request.form.get('password')
        elif self.request.method == 'GET':
            name = self.request.args.get('userName')
            password = self.request.args.get('password')
        self.verify.setName(name).setPasswd(password)
        self.verify.verifyName()
        self.verify.verifyPasswd()
        if self.verify.ifError():
            return False
        raws = self.dbSupport.findUser(name)
        if raws is None:
            self.verify.raiseVerifyError('LoginFailed','LoginFailed')
            return False
        for raw in raws:
            if self.verify.verifyLogin(raw.password):
                raw.tokenVersion = self.verify.updateVersion(raw.tokenVersion)
                self.dbSupport.setRaw(raw)
                self.token = self.generateToken(name,raw.tokenVersion)
                self.verify.raiseSuccessInf('success','Login successfully')
                return True
        return False

    def verifySignin(self):
        name = None
        password = None
        password2 = None
        if self.request.method == 'POST':
            name = self.request.form.get('userName')
            password = self.request.form.get('password')
            password2 = self.request.form.get('password2')
        elif self.request.method == 'GET':
            name = self.request.args.get('userName')
            password = self.request.args.get('password')
            password2 = self.request.args.get('password2')
        self.verify.setName(name).setPasswd(password).setPasswd2(password2)
        self.verify.verifySignIn()
        if self.verify.ifError():
            return False
        raws = self.dbSupport.findUser(name)
        if raws is not None:
            self.verify.raiseVerifyError('repeatedName','repeatedName')
            return False
        self.dbSupport.newUser(name,password)
        self.verify.raiseSuccessInf('success','signin successfully')
        self.verify.raiseSuccessInf('key',str(self.dbSupport.raw.keyPasswd))
        return True

    def verifyToken(self):
        token = None
        if self.request.method == 'POST':
            token = self.request.form.get('token')
        elif self.request.method == 'GET':
            token = self.request.args.get('token')
        if token is not None:
            data = self.verify.checkToken(token, self.KEY)
            if data is None:
                return False
            raws = self.dbSupport.findUser(data['userName'])
            if raws is not None:
                for raw in raws:
                    self.verify.verifyAccuracyWithToken(data,raw.tokenVersion,'version')
                    if self.verify.ifError():
                        return False
                    self.dbSupport.setRaw(raw)
                    self.name = data['userName']
                    return True
            self.verify.raiseVerifyError('tokenUnmatched','tokenUnmatched')
        else:
            self.verify.raiseVerifyError('tokenEmpty','toeknEmpty')
        return False

    def verifyHome(self):
        maxUserNum = None
        homeNum = None
        if self.request.method == 'POST':
            maxUserNum = self.request.form.get('maxUserNum')
            homeNum = self.request.form.get('homeNum')
        elif self.request.method == 'GET':
            maxUserNum = self.request.args.get('maxUserNum')
            homeNum = self.request.args.get('homeNum')
        self.home.setHomeNum(homeNum).setMaxUserNum(maxUserNum)
        homeResult = self.home.verifyHomeNum()
        maxResult = self.home.verifyMaxNum()
        if homeResult is None and maxResult is None:
            return False
        if maxResult is None:
            raw = self.dbSupport.findHome(homeNum)
            if raw is None:
                return False
            self.home.setUserNum(raw.numOfUsers)
            self.home.setMaxUserNum(raw.maxNumOfUsers)
            if self.home.verifyHome() is None:
                return False
            raw.numOfUsers += 1
            self.dbSupport.setRaw(raw)
            self.verify.raiseSuccessInf('success','set successfully')
        else:
            raws = self.dbSupport.findUser(self.home)
            for raw in raws:
                homeRaw = self.dbSupport.findHome(raw.roomNum)
                homeRaw.maxResult = maxResult
                self.dbSupport.setRaw(homeRaw)
                self.verify.raiseSuccessInf('success','set successfully')
        return True

    def verifyNewHome(self):
        homeNum = None
        boardCode = None
        if self.request.method == 'POST':
            homeNum = self.request.form.get('homeNum')
            boardCode = self.request.form.get('boardCode')
        elif self.request.method == 'GET':
            homeNum = self.request.args.get('homeNum')
            boardCode = self.request.args.get('boardCode')
        self.home.setHomeNum(homeNum).setBoardCode(boardCode)
        self.home.verifyHomeNum()
        if self.home.ifError() is True:
            return False
        self.home.verifyBoard()
        if self.home.ifError() is True:
            return False
        #hashCode = IOtool.toHash(boardCode)
        raw = self.dbSupport.findBoard(boardCode)
        if raw is None:
            self.home.raiseVerifyError('BoardError','BoardError')
            return False
        raw = self.dbSupport.findHome(homeNum)
        if raw is not None:
            self.home.raiseVerifyError('homeError','homeError')
            return False
        self.home.raiseSuccessInf('success','new home')
        return True

    def generateToken(self,name,version):
        body = {'userName': name, 'version': version}
        return self.verify.generateToken(self.KEY, 86400, body)