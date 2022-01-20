from pybotnet import ExternalScripts
from pybotnet.request import Request


script = ExternalScripts()


@script.add_script(script_name='echo_meta_data')
def echo_meta_data(request: Request, *args):
    """return meta_data"""
    return request.meta_data
