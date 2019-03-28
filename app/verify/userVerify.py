from app_2_0_0.app.toolbox.verifytool import VerifyFactory,VerifyTool,VerifyError

# it is a verify level for user information.
# the UserVerify class should be built by this factory
class UserVerifyFactory(VerifyFactory):
    def build(self):
        return UserVerify()

# it is inherited from VerifyError class and is overlord for user verification
# there is no need to use it, it has been packaged into UserVerify class
# However, the error type need to added if some customized error types is used in UserVerify
class UserVerifyError(VerifyError):
    def __init__(self,arg,type):
        super(UserVerifyError,self).__init__(arg,type)

    def feedback(self):
        if self.type == 'nameLength':
            self.msg = 'user name too long'
        elif self.type == 'nameBlank':
            self.msg = 'name can not be blank'
        elif self.type == 'passwdBlank':
            self.msg = 'password can not be blank'
        elif self.type == 'passwd2Blank':
            self.msg = 'please confirm the password'
        elif self.type == 'differentPasswd':
            self.msg = 'confirm password failed'
            self.msg = 'token has been out of time'
        elif self.type == 'BadSignature':
            self.msg = 'the token does not exited or is invalid'
        elif self.type == 'LoginFailed':
            self.msg = 'User name or password is not correct'
        elif self.type == 'tokenUnmatched':
            self.msg = 'The token is invalid or not matched'
        elif self.type == 'repeatedName':
            self.msg = 'The user name has been registered'
        elif self.type == 'tokenEmpty':
            self.msg = 'the token could not be blank'
        else:
            self.msg = 'UnknownProblem'
        return self.msg

# it is the main class of user verify level
# all of the private member has getter and setter
# iferror should not be used without a careful thinking
# error_index is a list of error raised in verify level, it can directly transfer into json file
# passwd2 is the password used to confirm the first passwd, prevent mistyping
class UserVerify(VerifyTool):
    def __init__(self):
        self.error_index = {'state':'error'}
        self.success_inf = {'state':'success'}
        self.name = None
        self.passwd = None
        self.passwd2 = None
        self.keyPasswd = None
        self.iferror = False

    # the raiseVerifyError function is overload
    # now the error tab and message will be collected into error_index
    # args and type is suggested to be the same though only type is the error tab
    def raiseVerifyError(self,args,type):
        try:
            raise UserVerifyError(args,type)
        except UserVerifyError as uve:
            temp = uve.feedback()
            self.error_index[type]=temp
            self.iferror=True
            print(temp)

    def raiseSuccessInf(self,key,value):
        self.success_inf[key] = value
        return self.success_inf

    # it is used to verify the sign in information
    # user name, password, password 2 and fridge code should be transferred.
    # it is a package of three verification method
    # it can not ensure any of the value be unique
    def verifySignIn(self):
        self.verifyName()
        self.verifyPasswds()

    # it is used to check the validity of token
    # it may be developed further in the future with a banned token list verification
    def checkToken(self,token,key):
        result,data = VerifyTool.verifyToken(token,token_key=key)
        if result == 'SignatureExpired':
            self.raiseVerifyError('SignatureExpired','SignatureExpired')
            return None
        elif result == 'BadSignature':
            self.raiseVerifyError('BadSignature','BadSignature')
            return None
        else:
            return data

    # it is used to verify the login information
    # to keep the generality of verify level, it is not linked to database
    # so it just verify the password is irregular or not
    def verifyLogin(self,mpasswd):
        if self.passwdVerify(self.passwd,mpasswd):
            return True
        else:
            self.raiseVerifyError('LoginFailed','LoginFailed')
            return False

    # it is used to verify weather the user name is valid or not
    # it just check the blank or length of the user name
    # the name should not longer than 20 characters
    # it should provided a method to change the limited size
    def verifyName(self):
        if not self.name:
            self.raiseVerifyError('nameBlank','nameBlank')
            return 'nameBlank'
        if len(self.name)>20:
            self.raiseVerifyError('nameLength','nameLength')
            return 'nameLength'
        else:
            return None

    # it is used to verify the passwords
    # it will check both of the password and password 2
    def verifyPasswds(self):
        if not self.passwd:
            self.raiseVerifyError('passwdBlank','passwdBlank')
            return 'passwdBlank'
        if not self.passwd2:
            self.raiseVerifyError('passwd2Blank','passwd2Blank')
            return 'passwd2Blank'
        if not VerifyTool.isequal(self.passwd2,self.passwd):
            self.raiseVerifyError('differentPasswd','differentPasswd')
            return 'differentPasswd'
        return None

    def verifyPasswd(self):
        if not self.passwd:
            self.raiseVerifyError('passwdBlank','passwdBlank')
            return 'passwdBlank'
        return None

    # it is used to verify weather the data store in token is the same as data in database
    # to keep the generality of verify level, it is not linked to database
    # so it need two data, which are extracted from database and token
    # loc is the key of data to check
    def verifyAccuracyWithToken(self,tokenData,cmpData,loc):
        if cmpData != tokenData[loc]:
            self.raiseVerifyError('tokenUnmatched','tokenUnmatched')
            return 'tokenUnmatched'
        else:
            return None

    # the followed methods are getter and setter of private members
    def setName(self,value):
        self.name = value
        return self
    def getName(self):
        return self.name
    def setPasswd(self,value):
        self.passwd = value
        return self
    def getPasswd(self):
        return self.passwd
    def setPasswd2(self,value):
        self.passwd2 = value
        return self
    def getPasswd2(self):
        return self.passwd2
    def getError(self):
        return self.error_index
    def ifError(self):
        return self.iferror
    def setKeyPasswd(self,value):
        self.keyPasswd = value
        return self
    def getKeyPasswd(self):
        return self.keyPasswd
    def getSuccess(self):
        return self.success_inf
