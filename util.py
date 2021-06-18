'''Common utilities'''

# import built-in & third-party modules
import requests


def make_send_message_api_url(TELEGRAM_TOKEN, ADMIN_CHAT_ID, message) -> str:
    '''
    return api url for send message \n
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"
    '''
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"


def post_data_by_third_party_proxy(url) -> bool:
    '''
    Send information using the http debugger site \n
    Only for special situations: \n
    Internet restrictions in some countries
    '''
    payload = {"UrlBox": url,
               "AgentList": "Mozilla Firefox",
               "VersionsList": "HTTP/1.1",
               "MethodList": "POST"
               }

    try:
        res = requests.post(
            url="https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx",
            data=payload,
            timeout=5)
        return res.status_code == 200

    except requests.exceptions.Timeout:
        return False
    except:
        return False
