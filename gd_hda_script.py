import hou, os
import os.path
from importlib import reload
from r_way_assignment_03.hou_to_gDrive import gDriveUtils
reload(gDriveUtils)

# get user input
usr_input = hou.pwd().parm("folder_name").evalAsString()
print(usr_input)

#instantiate class
utils = gDriveUtils.gDriveUtils()

#execute
def execute():
    utils.run(usr_input)