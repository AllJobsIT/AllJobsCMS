from datetime import datetime

from botmanager.basetask import TaskTemporarilyException, BotManagerBaseTask


class KITBaseTask(BotManagerBaseTask):
    TemporarilyException = TaskTemporarilyException

    def get_log_file_name(self):
        return "task{}-{:%Y-%m-%d-%H:%M:%S}".format(self.task.id, datetime.now())
