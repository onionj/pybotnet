
def simple_serializer(command, excepted_types:list[any]) ->tuple[list, str]:
    """
    try to conver args type
    
    return ([*arg], error | None)
    """
    if len(command) != len(excepted_types):
        return [], f"needs {len(excepted_types)} args bot {len(command)} are given"

    res = []
    for i, str in enumerate(command):
        try:
            res.append(excepted_types[i](str))
        except:
            return [], f"The {i} arg must be a {excepted_types[i]}"

    return res, None