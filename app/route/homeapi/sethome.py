from flask import request,jsonify
from app_2_0_0.app.support import dbSupportTool,verifySupportTool
from app_2_0_0.app.support.verifySupportTool import Type
from app_2_0_0.app.route.homeapi.blueprint import homeapi

@homeapi.route('/sethome',methods=['POST','GET'])
def sethome():
    verify = verifySupportTool.VerifySupportToolFactory().build()
    database = dbSupportTool.dbSupportToolFactory().build()
    verify.setDbSupport(database).setRequest(value=request)
    if verify.verifyToken() is False:
        return jsonify(verify.getError(Type.home)),404
    userRaw = database.getRaw()
    if verify.verifyHome() is False:
        return jsonify(verify.getError(Type.home)),404
    roomRaw = database.getRaw()
    database.load()
    userRaw.roomNumber = roomRaw.roomNumber
    database.setRaw(userRaw).load()
    return jsonify(verify.getSuccess(Type.home)),200