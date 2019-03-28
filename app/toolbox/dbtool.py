import string
from .basetool import BaseTool
import random

# DBToo is a toolbox class designed for database in flask.
# flask_sqlalchemy is suggested to be used as the database package
# help provide some comments on the methods
class DBTool(BaseTool):
    def _help(self):
        print('this is tool of database,include insert, drop')
        print('it has insert, drop, string2Bool, generate_token(not recommended),generate_randnum')
        print('use _helpfor to check some specific information')

    def _helpfor(self,fnc_name):
        if fnc_name == 'insert' or fnc_name == 'drop':
            print('to use them, a raw in the database and db need to be provided')
            print('like insert(raw,db), db is the instance of database')
        elif fnc_name == 'generate_token':
            print('it could generate a random number in the size of 10')
            print('it has not been developed completely, so it is not suggested to use')
        elif fnc_name == 'string2Bool':
            print('it is a function to convert string value of True, true, TRUE')
            print('into boolean value. Any other stirng value will return false')
        elif fnc_name == 'generate_randnum':
            print('it is a function to generate random number, position is the size of number')

    @classmethod
    def insert(cls,raw,db):
        db.session.add(raw)
        db.session.commit()

    @classmethod
    def drop(cls,raw,db):
        db.session.delete(raw)
        db.session.commit()

    @classmethod
    def generate_token(cls,table,db,size):
        min = int(pow(10.0,size-1))
        max = int(pow(10.0,size))
        newtoken = random.randint(min,max-1)
        return newtoken

    @classmethod
    def generate_randnum(cls,position):
        temp = ''.join(random.sample(string.digits,position))
        return temp

    @classmethod
    def string2Bool(cls,str):
        return (str == 'True' or str == 'TRUE' or str == 'true')
