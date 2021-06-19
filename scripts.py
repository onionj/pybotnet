'''Defult PyBotNet scripts'''

from time import sleep

scripts_name = {
    "do_sleep": 'do_sleep <scconds> <message>'
}


def execute_scripts(command, logger):
    command_name = command.split(' ')

    if command_name[0] in scripts_name:

        if command_name == 'do_sleep':
            return execute_do_sleep(command, logger)

    logger.info('invalid command')
    return False


def execute_do_sleep(command, logger):
    comm = command.split(' ')
    try:
        do_sleep(seconds=comm[1], logger=logger, sleep_message=comm[3])
        return True
    except:
        logger.error('execute_do_sleep invalid comman')
        return False


def do_sleep(seconds, logger, sleep_message=''):
    '''
    print sleep message and sleep
    '''
    print(sleep_message)
    logger.info(f'sleep {seconds} second | {sleep_message}')
    sleep(float(seconds))
    logger.info('sleep done')
