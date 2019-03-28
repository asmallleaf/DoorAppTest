from app_2_0_0.app.route.usrapi.signin import usrapi
from app_2_0_0.app.support import dbSupportTool,verifySupportTool
from app_2_0_0.app.support.verifySupportTool import Type
from flask import request,jsonify

@usrapi.route('/fdlogout',methods=['POST','GET'])
def fdlogout():
    verify = verifySupportTool.VerifySupportToolFactory().build()
    database = dbSupportTool.dbSupportToolFactory().build()
    verify.setDbSupport(database).setRequest(value=request)
    if verify.verifyToken() is False:
        return jsonify(verify.getError(Type.user)),404
    raw = database.getRaw()
    verify.verify.updateVersion(raw.tokenVersion)
    database.setRaw(raw).load()
    return jsonify(verify.getSuccess(Type.user)),200
