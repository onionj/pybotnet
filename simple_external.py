from pybotnet import ExternalScripts


script = ExternalScripts()


@script.add_script(script_name='test_3')
def test():
    """return test_3"""
    return "test_3"
