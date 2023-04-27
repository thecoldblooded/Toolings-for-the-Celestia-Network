import time

from constants import Emoji
from tasks import Task


def elapsed_to_string(since):
    elapsed = time.time() - since
    if elapsed >= 3600:
        hours = int(elapsed / 3600)
        minutes = int((elapsed % 3600) / 60)
        return f'{hours} hours and {minutes} minutes'
    elif elapsed >= 60:
        minutes = int(elapsed / 60)
        return f'{minutes} minutes'
    else:
        seconds = int(elapsed)
        return f'{seconds} seconds'


class ChainStuck(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'ChainStuck'
        self.prev_block_hash = None
        self.since = None
        self.stuck_block_count = 0

        try:
            self.chain.get_block_hash()
            self.method = self.chain.get_block_hash
        except:
            self.method = self.chain.get_height

    def run(self):
        block_hash = self.method()

        if self.prev_block_hash is None:
            self.prev_block_hash = block_hash
            self.since = time.time()
            return False

        if block_hash == self.prev_block_hash:
            self.stuck_block_count += 1
            elapsed_time = elapsed_to_string(self.since)
            return self.notify(f'Chain is stuck at block {block_hash} since {elapsed_time} ({self.stuck_block_count}) {Emoji.STUCK}')  # noqa

        if self.stuck_block_count > 0:
            elapsed_time = elapsed_to_string(self.since)
            self.notify(f'Chain come back in sync after {elapsed_time} ({self.stuck_block_count}) {Emoji.SYNC_OK}')

        self.prev_block_hash = block_hash
        self.since = time.time()
        self.stuck_block_count = 0
        return False
