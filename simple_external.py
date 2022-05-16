from pybotnet import ExternalScripts
from pybotnet.request import Request


external_botnet = ExternalScripts()


@external_botnet.add_script(script_name='echo_meta_data', script_version="0.1.0")
def echo_meta_data(request: Request, *args):
    """return meta_data"""
    return request.meta_data
