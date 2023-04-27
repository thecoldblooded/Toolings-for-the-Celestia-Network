from constants import Emoji, CPU_LIMIT, RAM_LIMIT, DISK_LIMIT, LOG_SIZE_THRESHOLD
from tasks import Task
from utils import System, to_gb, run_command


class CpuAlert(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'CpuAlert'

    def run(self):
        cpu_usage = System().get_usage().cpu_usage

        if cpu_usage > CPU_LIMIT:
            return self.notify('CPU usage is above %d%% (%d%%) %s' % (CPU_LIMIT, cpu_usage, Emoji.CPU))

        return False


class RamAlert(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'RamAlert'

    def run(self):
        usage = System().get_usage()

        ram_used = round(usage.ram_used / usage.ram_size * 100, 1)
        if ram_used > RAM_LIMIT:
            return self.notify('Ram usage is above %d%% (%d%%) %s' % (RAM_LIMIT, ram_used, Emoji.RAM))

        return False


class DiskAlert(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'DiskAlert'

    def run(self):
        usage = System().get_usage()

        if usage.disk_percentage_used <= DISK_LIMIT:
            return False

        return self.notify(
            'Disk usage is above %d%% (%d%%) (/var/log: %.1fG, /: %.1fG) %s' %
            (DISK_LIMIT, usage.disk_percentage_used, to_gb(usage.disk_used_by_log), to_gb(usage.disk_used),
             Emoji.DISK))

    def can_recover(self):
        return to_gb(System().get_usage().disk_used_by_log) > LOG_SIZE_THRESHOLD

    def recover(self):
        run_command('truncate -s 0 /var/log/syslog')
        run_command('rm /var/log/syslog.*')
        run_command('rm -r /var/log/journal/*')
