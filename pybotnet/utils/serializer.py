
def simple_serializer(command, excepted_types:list[any]) ->tuple[list, str]:
    """
    try to conver args type
    
    return ([*arg], error | None)
    """
    if len(command) != len(excepted_types):
        return [], f"needs {len(excepted_types)} args bot {len(command)} are given, \n\nyou send:\n {command}"

    res = []
    for i, string in enumerate(command):
        try:
            res.append(excepted_types[i](string))
        except:
            return [], f"The arg[{i}] must be a {excepted_types[i]}, you send: {string}, \n see: `/help script_name`"

    return res, None