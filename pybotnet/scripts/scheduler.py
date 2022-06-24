import os
import logging
import schedule
import threading

from .. import BotNet, Request, UserException

# TODO: return command outputs

_logger = logging.getLogger(f"__{__name__}   ")

@BotNet.default_script(script_version="0.0.1")
def scheduler(request: Request) -> str:
    """`
    Starts a new schedule for a command.

    syntax:
        `/schedule start <second> <shell-command>`
        `schedule list`: lists all schedules
        `schedule stop <schedule_id>`: Stops a schedule

    Note:
        Scheduling is runing in RAM,
        if the system is turned off all schedules are cleared
    """

    if len(request.command) == 0:
        raise UserException("invalid command") 

    if request.command[0] == "start":
        if len(request.command) < 2:
            raise UserException("need second and command params ") 

        second = request.command[1]
        command = ' '.join(request.command[2:])

        scheduler_util = ScheduleManagement(int(second), command)

        schedule_id = scheduler_util.next_id
        scheduler_util.next_id += 1

        scheduler_util.listOfSchedules[schedule_id] = [threading.Thread(target=scheduler_util.startSchedule), second, command]
        
        # starts threading object
        scheduler_util.listOfSchedules[schedule_id][0].start()

        _logger.info(
            f"Started Schedule {command} , will run each {second} second")
        return f"Started Schedule {command} , will run each {second} second"

    elif request.command[0] == "list":
        listOfSchedules_ToReturn = []
        for key, value in ScheduleManagement.listOfSchedules.items():
            listOfSchedules_ToReturn.append(
                f"schedule_id = {key} command {value[2]}, Will run each {value[1]} second")
        return "\n".join(listOfSchedules_ToReturn)

    elif request.command[0] == "stop":
        listOfSchedules = ScheduleManagement.listOfSchedules
        if len(request.command) < 1:
            raise UserException("/schedule stop, error: need schedule_id") 

        schedule_id = request.command[1:]

        if schedule_id not in ScheduleManagement.listOfSchedules.keys():
            _logger.error(f"Schedule {schedule_id} is not available")
            return f"Schedule {schedule_id} is not available"

        _logger.info(f"Stopping Schedule {schedule_id}")

        threadObject = listOfSchedules[schedule_id][0]
        listOfSchedules.pop(schedule_id)
        threadObject.kill()

        _logger.info(f"Schedule {schedule_id} stopped.")
        return f"Schedule {schedule_id} stopped."

    else:
        raise UserException(f"/schedule don't have {request.command[0]}")


class ScheduleManagement:
    listOfSchedules = {}
    next_id = 0

    def __init__(self, second, command):
        self.second = second
        self.command = command

    def startSchedule(self):
        try:
            schedule.every(self.second).seconds.do(os.system, self.command)
            while self.command in self.listOfSchedules.keys():
                schedule.run_pending()
        except:
            self.listOfSchedules.pop(self.command)

