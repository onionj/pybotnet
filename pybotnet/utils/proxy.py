import random

from .third_party_proxy import httpdebugger

# from third_party_proxy import reqbin


_proxy_list = [httpdebugger]

# TODO: add multi proxy and choice best proxy
def http_request(
    method: str, url: str, data: dict = None, headers: dict = None, timeout=10
):
    """choice best proxy and make http reuest"""

    return random.choice(_proxy_list).http_request(
        method=method, url=url, data=data, headers=headers, timeout=timeout
    )
