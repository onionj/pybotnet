import os
import time
import logging
import schedule
import threading

from .. import BotNet, Request, UserException

_logger = logging.getLogger(f"__{__name__}   ")

@BotNet.default_script(script_version="0.0.1", script_name="schedule")
def scheduler(request: Request) -> str:
    """`
    Starts a new schedule for a command.

    syntax:
        `/schedule start <second> <shell-command>`
        `/schedule list`: lists all schedules
        `/schedule stop <schedule_ids>`: Stops that's schedules

    example command:
        /schedule start echo test >> test.txt
        /schedule list
        /schedule stop 0


    Note:
        Scheduling is runing in RAM,
        if the system is turned off all schedules are cleared
    """

    if len(request.command) == 0:
        raise UserException("invalid command") 

    if request.command[0] == "start":
        if len(request.command) < 2:
            raise UserException("need second and command params ") 

        try:
            second = int(request.command[1])
        except:
            raise UserException("The second must be a number")
        command = ' '.join(request.command[2:])

        # create new schedule management instance
        schedule_management = ScheduleManagement(second, command)

        # add schedule management thread to scehdules list
        schedule_management.listOfSchedules[schedule_management.id] = (threading.Thread(target=schedule_management.startSchedule), second, command)
        
        # starts threading object
        schedule_management.listOfSchedules[schedule_management.id][0].start()

        _logger.debug(
            f"Started Schedule {command} , will run each {second} second")
        return f"Started Schedule {command} , will run each {second} second"

    elif request.command[0] == "list":
        listOfSchedules_ToReturn = []
        for key, value in ScheduleManagement.listOfSchedules.items():
            listOfSchedules_ToReturn.append(
                f"""id:{key}
                command:{value[2]}
                run each {value[1]} second
------""")
        return "\n".join(listOfSchedules_ToReturn)

    elif request.command[0] == "stop":
        listOfSchedules = ScheduleManagement.listOfSchedules

        if len(request.command) < 1:
            raise UserException("/schedule stop, error: need schedule_id") 

        schedule_ids = request.command[1:]

        for schedule_id in schedule_ids:
            if schedule_id not in listOfSchedules.keys():
                _logger.debug(f"Schedule {schedule_id} is not available")
                return f"Schedule {schedule_id} is not available"

            _logger.debug(f"Stopping Schedule {schedule_id}")

            listOfSchedules.pop(schedule_id)

            _logger.debug(f"Schedule {schedule_id} stopped.")
        return f"Schedules {schedule_ids} stopped."

    else:
        raise UserException(f"/schedule don't have {request.command[0]}, use start,list,stop")


class ScheduleManagement:
    listOfSchedules = {}
    next_id = 0

    def __init__(self, second, command):
        self.second = second
        self.command = command
        self.id = self.get_id()
    
    def get_id(self):
        id = ScheduleManagement.next_id
        ScheduleManagement.next_id += 1
        return str(id)

    def startSchedule(self):
        try:
            job = schedule.every(self.second).seconds.do(os.system, self.command)
            while self.id in ScheduleManagement.listOfSchedules.keys():
                schedule.run_pending()
            schedule.cancel_job(job)
            
        except:
            ScheduleManagement.listOfSchedules.pop(self.schedule_id)

