from app_2_0_0.app.toolbox.verifytool import VerifyTool as vt

# this is a irregular verify level class inherited from Verify Toolbox
# it should use Factory method and will be redeveloped in the future
# it is used to provide verify methods for data transferred into database
class Verify(vt):
    # check method is only a package of VerifyTool and VerifyError
    # it will check weather the size of items in a list or dictionary is in a section of max and min value
    # if success, it will return the size of items
    # if failed, it will raise error and return false
    # the function is not well-designed and should be improved in the future
    @classmethod
    def check(cls,items,max,min,error_arg,error_tab):
        result,item_num = cls.checkNum(items,max_num=max,min_num=min)
        if result:
            return item_num
        else:
            vt.raiseVerifyError(error_arg,error_tab)
            return False

    # check2 has the same function as check2
    # the only difference between the two methods is that it can only compare a single value
    # weather it is bigger than val or smaller than val. it is set to compare is upper val in default
    @classmethod
    def check2(cls,items,val,upper,error_arg,error_tab):
        result,item_num = cls.checkNum2(items,order_num=val,is_upper=upper)
        if result:
            return item_num
        else:
            vt.raiseVerifyError(error_arg,error_tab)
            return False