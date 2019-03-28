from abc import abstractmethod

# this is a abstract class. Toolbox class should inherited from it
# _help and _helpfor method should be implemented to provide a clear help comments
class BaseTool():
    @abstractmethod
    def _help(self):
        print('this is a toolbox and will be enriched in the future\n')

    @abstractmethod
    def _helpfor(self,fnc_name):
        print('you can use this to get help() for specific function\n')

# this is a abstract class. ErrorBox class could inherited from it
# it was specific for RuntimeError
class BaseError(RuntimeError):
    def __init__(self,args):
        self.args = args

    def __str__(self):
        return self.args

class SupportToolFactory():
    @abstractmethod
    def build(self):
        pass

class SupportTool():
    @abstractmethod
    def _help(self):
        pass
