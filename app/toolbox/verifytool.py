from .basetool import BaseTool,BaseError
import abc
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as time_token
from itsdangerous import SignatureExpired,BadSignature

# this is a abstract class, which is defined due to Factory method
# ALl of the class in VerifyTool is suggested to be inherited for a specific concept
class VerifyFactory():
    @abc.abstractmethod
    def build(self):
        pass

# VerifyTool is a toolbox designed for verification
# the original verification is designed to build a user verification level
# most of the comments has been collected in _helpfor function
# the raiseVerifyError is suggested to be overload when inheriting to generate a error list.
class VerifyTool(BaseTool):
    def _help(self):
        print('this is a tool for Verify class, developing')
        print('till now, has fnc isequal, raiserVerifyError, isnone, checkNum, checkNum2')
        print('passwdVerify,generateToken,verifyToken')
        print('class VerifyError')

    def _helpfor(self,fnc_name):
        if fnc_name == 'checkNum'or fnc_name == 'checkNum2':
            print('There are two overloading funcs.\nif min>max, the interval will be x<=min and x>=max')
            print('if min<=max, it will be min<=x<=max\n you also can user x>ordered num or x<num')
        elif fnc_name == 'isequal':
            print('just meaningless')
        elif fnc_name == 'raiseVerifyError':
            print('used to raise error, args is the tab, type is the label in class VerifyError')
            print('when you have customized a label, you need to add it in the class.')
        elif fnc_name == 'isnone':
            print('it is used to check the blank key in a index. using if not')
            print('can detect '',none,0,false.... and return the blank key as a list')
        elif fnc_name == 'passwdVerify':
            print('this is a password verify tool, need input the password and the hash version')
        elif fnc_name == 'generateToken':
            print('this is used to generate token, need the expiration time and additional index if needed')
        elif fnc_name == 'verifyToken':
            print('this is used to verify user token, only need the token serial and return the loaded data '
                  'if succeeds')

    @classmethod
    def isequal(cls,new,old):
        if new == old:
            return True
        else:
            return False

    @classmethod
    def raiseVerifyError(cls,args,type):
        try:
            raise VerifyError(args,type)
        except VerifyError as ve:
            print(ve.feedback())

    @classmethod
    def isnone(cls,elments):
        blanks=[]
        for key,value in elments.items():
            if not value:
                blanks.append(key)
        return blanks

    @classmethod
    def checkNum(cls,items,max_num,min_num):
        item_num = len(items)
        if min_num>max_num:
            if item_num<=min_num and item_num>=max_num:
                return True,item_num
            else:
                return False
        else:
            if item_num>=min_num and item_num<=max_num:
                return True,item_num
            else:
                return False

    @classmethod
    def checkNum2(cls,items,order_num,is_upper):
        item_num = len(items)
        if is_upper == True:
            if item_num>= order_num:
                return True,item_num
            else:
                return False
        else:
            if item_num<order_num:
                return True,item_num
            else:
                return False

    @classmethod
    def cmpNum(cls,num,order_num,is_upper):
        if is_upper == True:
            if num>= order_num:
                return True
            else:
                return False
        else:
            if num<order_num:
                return True
            else:
                return False
    # this method will verify password with the hash encoded value
    @classmethod
    def passwdVerify(cls,passwd,hash_passwd):
        return pwd_context.verify(passwd,hash_passwd)

    @classmethod
    def generateToken(cls,secret_key,expiration,index):
        token_serial = time_token(secret_key,expires_in=expiration)
        return token_serial.dumps(index)

    def updateVersion(self,version):
        num = int(version)
        if num>=255:
            num = 0
        else:
            num += 1
        return num

    @classmethod
    def verifyToken(cls,token_serial,token_key):
        token_cmp = time_token(token_key)
        try:
            data = token_cmp.loads(token_serial)
        except SignatureExpired:
            return 'SignatureExpired',None
        except BadSignature:
            return 'BadSignature',None
        return 'Success',data

# the verifyError class is suggested to be inherited since the error type need to be customized
# if inherited, feedback method should be overload and implemented as the following structure
# if self.type == 'error tab':
#    self,msg = 'error message'
# the type and message will be returned by raiseVerifyError
class VerifyError(BaseError):
    msg = None

    def __init__(self,args,type):
        super(VerifyError,self).__init__(args)
        self.type = type

    def feedback(self):
        if self.type == 'PasswdUnadmit':
            self.msg = 'the passwd is not correct, meet error PasswdUnadmit'
        elif self.type == 'NotLogin':
            self.msg = 'the user has not logined yet, meet error NotLogin'
        elif self.type == 'IllegalArgs':
            self.msg = 'there are some arguments that does not meet the requirments'
        elif self.type == 'MutilableObjects':
            self.msg = 'there is mutilable objects when verify the number of the objects'
        else:
            self.msg = 'Unknown error happened, Unknown Error in VerifyError'
        return self.msg
