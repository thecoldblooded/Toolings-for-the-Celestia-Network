import time

from telegram import TelegramNotification


def seconds(m):
    return m


def minutes(m):
    return m * 60


def hours(h):
    return h * 60 * 60


class Task:
    def __init__(self, chain):
        self.name = ''
        self.chain = chain
        self.check_every = minutes(5)
        self.notify_every = minutes(5)
        self.recover_every = hours(1)

        self.last_check = 0
        self.last_notify = 0
        self.last_recover = 0

    def should_be_checked(self):
        return (self.last_check + self.check_every) < time.time()

    def should_be_notified(self):
        return (self.last_notify + self.notify_every) < time.time()

    def mark_checked(self):
        self.last_check = time.time()

    def notify(self, notification_str, no_check=False):
        if self.should_be_notified() or no_check:
            self.last_notify = time.time()
            TelegramNotification().append_message(notification_str)
            return True
        return False

    def run(self):
        raise Exception('Abstract run()')

    def should_be_recovered(self):
        return (self.last_recover + self.recover_every) < time.time()

    def can_recover(self):
        return False

    def recover(self):
        return None

    def mark_recovered(self):
        self.last_recover = time.time()

