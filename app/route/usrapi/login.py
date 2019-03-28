from app_2_0_0.app.route.usrapi.blueprint import usrapi
from app_2_0_0.app.support import dbSupportTool,verifySupportTool
from app_2_0_0.app.support.verifySupportTool import Type
from flask import request,jsonify

@usrapi.route('/fdlogin',methods=['POST','GET'])
def fdLogin():
    verify = verifySupportTool.VerifySupportToolFactory().build()
    database = dbSupportTool.dbSupportToolFactory().build()
    verify.setDbSupport(database).setRequest(request)

    if verify.verifyLogin() is False:
        return jsonify(verify.getError(Type.user)),404
    database.load()
    json = verify.getSuccess(Type.user)
    json['token'] = verify.token.decode('ascii')
    return jsonify(json),200

