from app_2_0_0.app.route.usrapi.login import usrapi
from app_2_0_0.app.support import dbSupportTool,verifySupportTool
from app_2_0_0.app.support.verifySupportTool import Type
from flask import request,jsonify

@usrapi.route('/fdsignin',methods=['POST','GET'])
def fdsignin():
    verify = verifySupportTool.VerifySupportToolFactory().build()
    database = dbSupportTool.dbSupportToolFactory().build()
    verify.setDbSupport(database).setRequest(value=request)
    #print(verify.request)
    if verify.verifySignin() is False:
        return jsonify(verify.getError(Type.user)),404
    database.load()
    return jsonify(verify.getSuccess(Type.user)), 200
