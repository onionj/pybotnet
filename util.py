'''Common utilities'''

# import built-in & third-party modules
from configs import TELEGRAM_TOKEN
import requests
import json

from bs4 import BeautifulSoup


def make_send_message_api_url(TELEGRAM_TOKEN, ADMIN_CHAT_ID, message) -> str:
    '''
    return api url for send message \n
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"
    '''
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"


def post_data(url, logger) -> bool:
    '''return False or response\n'''
    try:
        response = requests.post(url=url, timeout=5)
        if response.status_code == 200:
            logger.info('post_data data sended response: 200')
            return response

        logger.error(
            f'post_data error: data not sended response: {response.status_code}')
        return False

    except requests.exceptions.Timeout:
        logger.error(f'post_data error: timeout ')
        return False
    except:
        logger.error(f'post_data Unknown error')
        return False


def post_data_by_third_party_proxy(url, logger):
    '''
    return False or response \n
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
        response = requests.post(
            url="https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx",
            data=payload,
            timeout=5)

        if response.status_code == 200:
            logger.info(
                'post_data_by_third_party_proxy data sended response: 200')
            return response

        logger.error(
            f'post_data_by_third_party_proxy error: data not sended response: {response.status_code}')
        return False

    except requests.exceptions.Timeout:
        logger.error(f'post_data_by_third_party_proxy error: timeout ')
        return False
    except:
        logger.error(f'post_data_by_third_party_proxy Unknown error')
        return False


def get_update_by_third_party_proxy(TELEGRAM_TOKEN, logger):
    '''Get the latest messages sent to the bot in the last 24 hours by third party proxy'''

    get_updates_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/Getupdates"

    response = post_data_by_third_party_proxy(
        get_updates_api_url, logger)

    if not response:
        logger.error(
            'get_command_by_third_party_proxy > post_data_by_third_party_proxy return False')
        return False

    try:

        response_source = response.text
        response_source = BeautifulSoup(response_source, "html.parser")
        response_source = response_source.find("div", id="ResultData").text

        if 'The remote server returned an error' in response_source:
            logger.error(
                f'get_update_by_third_party_proxy [False TOKEN or ADMIN_CHAT_ID] error: {response_source}')
            return False

        response_source = response_source.replace("Response Content", "")
        response_source = response_source.replace("edited_message", "message")
        response_source = json.loads(response_source)['result']
        return response_source
    except:
        logger.error(
            'get_update_by_third_party_proxy error Data extraction failed')
        return False


def get_last_update_id(messages: list, ADMIN_CHAT_ID: str, logger):

    if messages == []:
        return False

    # get last admin message and return update_id
    for message in messages[::-1]:
        try:
            last_message_chat_id = str(message['message']['chat']['id'])
            update_id = str(message["update_id"])
            if last_message_chat_id == ADMIN_CHAT_ID:
                return update_id
        except:
            continue

    # try to get last update_id and return
    last_message = messages.pop()
    try:
        return str(last_message["update_id"])
    except:
        logger.error(
            'get_last_update_id Failed to extract the latest update_id')
        return False


def set_message_ofset(messages: list, TELEGRAM_TOKEN: str, ADMIN_CHAT_ID: str, logger) -> None:

    update_id = get_last_update_id(messages, ADMIN_CHAT_ID, logger)

    if update_id:
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/Getupdates?offset={update_id}"

        if post_data_by_third_party_proxy(api_url, logger):
            logger.info(f'Setـmessageـtoـread Message_id: {update_id} DONE')
            return

    logger.error('set_message_ofset Failed')


def extract_last_admin_command(messages: list, ADMIN_CHAT_ID: str, TELEGRAM_TOKEN: str,  logger):

    message_text = False

    for message in messages[::-1]:
        try:
            last_message_chat_id = str(message['message']['chat']['id'])
            last_text = message['message']['text']

        except:
            continue

        if last_message_chat_id == ADMIN_CHAT_ID:
            logger.info(
                f' -message from admin: {last_text}')
            message_text = last_text
            break
        logger.info(f' -message from {last_message_chat_id}: {last_text}')

    set_message_ofset(messages, TELEGRAM_TOKEN, ADMIN_CHAT_ID, logger)

    return message_text
