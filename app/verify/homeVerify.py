from app_2_0_0.app.toolbox.verifytool import VerifyFactory,VerifyTool,VerifyError

class HomeVerifyFactory(VerifyFactory):
    @classmethod
    def build(cls):
        return HomeVerify()

class HomeVerifyError(VerifyError):
    def __init__(self,arg,type):
        super(HomeVerifyError,self).__init__(arg,type)

    def feedback(self):
        if self.type == 'homeBlank':
            self.msg = 'Home number can not be blank'
        elif self.type == 'userBlank':
            self.msg = 'user number can not be empty'
        elif self.type == 'maxUserBlank':
            self.msg = 'max user number can not be empty'
        elif self.type == 'userError':
            self.msg = 'user number is not digit'
        elif self.type == 'maxUserError':
            self.msg = 'max user number is not digit'
        elif self.type == 'homeError':
            self.msg = 'home number is invalid'
        elif self.type == 'userFull':
            self.msg = 'the room is full of person'
        elif self.type == 'BoardError':
            self.msg = 'Board code is invalid'
        else:
            self.msg = 'Unknown Error'
        return self.msg

class HomeVerify(VerifyTool):
    def __init__(self):
        self.error_index = {'state':'error'}
        self.success_inf = {'state':'success'}
        self.iferror = False
        self.homeNum = None
        self.userNum = None
        self.maxUserNum = None
        self.boardCode = None

    def raiseVerifyError(self,args,type):
        try:
            raise HomeVerifyError(args,type)
        except HomeVerifyError as uve:
            temp = uve.feedback()
            self.error_index[type]=temp
            self.iferror=True
            print(temp)

    def raiseSuccessInf(self,key,value):
        self.success_inf[key] = value
        return self.success_inf

    def verifyHomeNum(self,):
        if self.homeNum.isdigit() is False:
            self.raiseVerifyError('homeError','homeError')
            return None
        if self.homeNum is None:
            self.raiseVerifyError('homeBlank','homeBlank')
            return None
        if len(self.homeNum) != 8:
            self.raiseVerifyError('homeError','homeError')
            return None
        return True

    def verifyUserNum(self):
        if self.userNum is None:
            self.raiseVerifyError('userBlank','userBlank')
            return None
        if self.userNum.isdigit() is False:
            self.raiseVerifyError('userError','userError')
            return None
        return True

    def verifyMaxNum(self):
        if self.maxUserNum is None:
            self.raiseVerifyError('maxUserBlank','maxUserBlank')
            return None
        if self.maxUserNum.isdigit() is False:
            self.raiseVerifyError('maxUserError','maxUserError')
            return None
        return True

    def verifyHome(self):
        if self.cmpNum(self.userNum,self.maxUserNum,True):
            self.raiseVerifyError('userFull','userFull')
            return None
        return True

    def verifyBoard(self):
        if self.boardCode is None:
            self.raiseVerifyError('BoardError','BoardError')
            return None
        return True

    def setBoardCode(self,value):
        self.boardCode = value
        return self
    def getBoardCode(self):
        return self.boardCode
    def setHomeNum(self,value):
        self.homeNum = value
        return self
    def getHomeNum(self):
        return self.homeNum
    def setUserNum(self,value):
        self.userNum = value
        return self
    def getUserNum(self):
        return self.userNum
    def setMaxUserNum(self,value):
        self.maxUserNum = value
        return self
    def getMaxUserNum(self):
        return self.maxUserNum
    def getError(self):
        return self.error_index
    def ifError(self):
        return self.iferror
    def getSuccess(self):
        return self.success_inf