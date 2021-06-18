'''Common utilities'''

# import built-in & third-party modules
import requests


def post_data_by_third_party_proxy(URL):
    '''
    Send information using the http debugger site \n
    Only for special situations: \n
    Internet restrictions in some countries
    '''
    payload = {"UrlBox": URL,
               "AgentList": "Mozilla Firefox",
               "VersionsList": "HTTP/1.1",
               "MethodList": "POST"
               }

    res = requests.post(
        "https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx", payload)
    return res
