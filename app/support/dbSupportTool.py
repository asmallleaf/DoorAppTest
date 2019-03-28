from app_2_0_0.app.toolbox.basetool import SupportTool,SupportToolFactory
from app_2_0_0.app.toolbox.dbtool import DBTool
from app_2_0_0.app.toolbox.iotool import IOtool
from app_2_0_0.app.database.models import db,users,rooms,boards

class dbSupportToolFactory(SupportToolFactory):
    def build(self):
        return dbSupportTool()

class dbSupportTool(SupportTool):
    def __init__(self):
        self.db = db
        self.raw = None

    def setDatabase(self,value):
        self.db = value
        return self

    def getDatabase(self):
        return self.db

    def findUser(self,name):
        raws = self.db.session.query(users).filter(users.userName==name).all()
        if not raws:
            return None
        else:
            return raws

    def findHome(self,homeNum):
        raw = self.db.session.query(rooms).filter(rooms.roomNumber==homeNum).first()
        if raw is not None:
            return raw
        else:
            return None

    def findBoard(self,code):
        raw = self.db.session.query(boards).filter(boards.codes == code).first()
        if raw is not None:
            return raw
        else:
            return None

    def newUser(self,name,password):
        key = self.generateKey()
        hashPasswd = IOtool.toHash(password)
        self.raw = users(userName=name,password=hashPasswd,keyPasswd=key,tokenVersion=0)
        return self

    def newRoom(self,roomNum,max,number):
        self.raw = rooms(doorState=False,maxNumOfUsers=max,roomNumber=roomNum,numOfUsers=number)
        return self

    def generateKey(self):
        key = DBTool.generate_randnum(8)
        raw = self.db.session.query(users).filter(users.keyPasswd==key).first()
        if raw:
            return self.generateKey()
        else:
            return key

    def setRaw(self,value):
        self.raw = value
        return self
    def getRaw(self):
        return self.raw

    def load(self):
        DBTool.insert(self.raw,self.db)
        return self