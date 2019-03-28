from .basetool import BaseTool
from json import JSONEncoder
from passlib.apps import custom_app_context as pwd_context
import datetime

# IOtool is a class designed for Input or Output stream.
# some format conversion methods are provided
class IOtool(BaseTool):
    def _help(self):
        print('this is a toolbox for IO problem')
        print('Till now, has fnc toJson, toHash,class JsonEncoder')

    def _helpfor(self,fnc_name):
        if fnc_name == 'toJson':
            print('this is developed for sqlalchemy, the object should be ')
            print('model class from sqlalchemy')
        elif fnc_name == 'JsonEncoder':
            print('this is a class inherit from JSONEncoder, please inherit it if needed')
            print('has defined the encoder way of datetime class')
        elif fnc_name == 'toHash':
            print('this is a function to translate passwd to Hash')

    # it is used to change a class into the one that can be encoded by jsonify
    # _sa_instance_state is the foreign key in a sqlalchemy class, which should be deleted from the class
    @classmethod
    def toJson(cls,object):
        dict = object.__dict__
        if '_sa_instance_state' in dict:
            del dict['_sa_instance_state']
        return dict

    @classmethod
    def toHash(cls,passwd):
        return pwd_context.encrypt(passwd)


# this is a class that should be collected in IOtool but also can be an isolated class
# it is used to customized the JsonEncode in jsonify package
# the transfer of time stamp is converted into time string
class JsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, obj)

