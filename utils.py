from subprocess import PIPE, Popen

from constants import HAS_TIMEOUT, MOUNT_POINT


def to_gb(size):
    return size / 1024 / 1024


def to_mb(size):
    return size / 1024


def to_pretty_size(size):
    v = size / 1024
    if v > 1024:
        return '%.1f GB' % (v / 1024.)
    else:
        return '%d MB' % (int(v))


def run_command(command, stdout=PIPE):
    stdout, stderr = Popen(command, shell=True, stdout=stdout, stdin=PIPE).communicate()
    if stdout:
        return stdout.strip().decode(encoding='UTF-8')
    return ''


class SystemUsage:
    uptime = ''
    disk_size = 0
    disk_used = 0
    disk_used_by_log = 0
    disk_percentage_used = 0

    ram_size = 0
    ram_used = 0
    ram_free = 0

    cpu_usage = 0

    def __str__(self):
        return '\tUptime: %s\n\tDisk (size, used, %%): %.1fG %.1fG %d%% (/var/log: %.1fG)\n\tRam (size, used, free): %.1fG %.1fG %.1fG\n\tCPU: %d%%' % (  # noqa
            self.uptime,
            to_gb(self.disk_size), to_gb(self.disk_used), self.disk_percentage_used,
            to_gb(self.disk_used_by_log),
            to_gb(self.ram_size), to_gb(self.ram_used), to_gb(self.ram_free),
            self.cpu_usage)

    def __repr__(self):
        return self.__str__()


class System:
    def __init__(self):
        self.mount_point = MOUNT_POINT

    def get_ip(self):  # noqa
        """ Return IP address """
        return run_command('ip addr').rsplit('inet ', 1)[-1].split('/')[0]

    def get_service_uptime(self):  # noqa
        return " ".join(
            run_command(f"systemctl status celestia_tool").split('\n')[2].split(";")[-1].strip().split()[:-1]
        )

    def get_usage(self):
        """ Returns a usage object """
        u = SystemUsage()
        u.uptime = run_command('uptime').split('up ')[1].split(',')[0]
        u.disk_size = int(run_command(f'df {self.mount_point}').split('\n')[1].split()[1])
        u.disk_used = int(run_command(f'df {self.mount_point}').split('\n')[1].split()[2])
        u.disk_percentage_used = float(
            run_command(f'df {self.mount_point}').split('\n')[1].split()[4].replace('%', ''))
        u.disk_used_by_log = int(run_command('du /var/log').rsplit('\n', 1)[-1].split()[0])

        u.ram_size = int(run_command('free').split('\n')[1].split()[1])
        u.ram_used = int(run_command('free').split('\n')[1].split()[2])
        u.ram_free = int(run_command('free').split('\n')[1].split()[4])

        u.cpu_usage = float(run_command('top -b -n 1 | grep Cpu').split()[1].replace(',', '.'))
        return u
