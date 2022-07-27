from pybotnet import ExternalScripts, Context, simple_serializer, UserException

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


@external_botnet.add_script(script_name="sys_data", script_version="0.1.0")
def get_system_info(context: Context):
    """return system_info"""
    sys_data = ""
    for key, value in context.system_info().items():
        sys_data += f"{key}: {value}\n"
    return sys_data


@external_botnet.add_script()
def counter(context: Context):
    """
    count numbers
    syntax:
        `/counter [number]`
    example:
        `/counter 10`
    """

    # serializer user input
    command, error = simple_serializer(context.command, [int])
    if error:
        raise UserException(error)

    new_number = command[0]

    counter = context.get_global_value("counter")
    if counter:
        new_counter = counter + new_number
        context.set_global_value("counter", new_counter)
        return new_counter
    context.set_global_value("counter", new_number)
    return new_number


# step (3)
# example: whe import `external_botnet` in `simple.py` file and
#  run `botnet.import_external_scripts(external_botnet)`
