from flask import request,jsonify
from app_2_0_0.app.support import dbSupportTool,verifySupportTool
from app_2_0_0.app.support.verifySupportTool import Type
from app_2_0_0.app.route.homeapi.sethome import homeapi

@homeapi.route('/newhome',methods=['POST','GET'])
def newhome():
    verify = verifySupportTool.VerifySupportToolFactory().build()
    database = dbSupportTool.dbSupportToolFactory().build()
    verify.setDbSupport(database).setRequest(value=request)
    if verify.verifyNewHome() is False:
        return jsonify(verify.getError(Type.home)),404
    database.newRoom(max=1,number=0,roomNum=verify.home.getHomeNum()).load()
    return jsonify(verify.getSuccess(Type.home)),200
