from app_2_0_0.app.route.usrapi.logout import usrapi
from app_2_0_0.app.route.homeapi.newhome import homeapi

# ALl of the blueprints will be collected here
# the source of each blueprint should be updated if there is a new api built
# the createapp will import the webapi and usrapi from this file

usrapi = usrapi
homeapi = homeapi
