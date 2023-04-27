import sys
import time
import traceback

from custom_logging import logger
from system_alert import CpuAlert, RamAlert, DiskAlert
from chain_stuck import ChainStuck
from chains import CelestiaNode
from constants import Emoji, AUTO_RECOVER, SLEEP_TIME
from telegram import TelegramNotification

if sys.version_info[0] < 3:
    print('python2 not supported, please use python3')
    sys.exit(0)

TASKS = [CpuAlert, RamAlert, DiskAlert, ChainStuck]


def main():
    tasks = []
    chain = CelestiaNode()
    for task in TASKS + chain.CUSTOM_TASKS:
        tasks.append(task(chain))

    message = f'Celestia tool started {Emoji.START}\nEnabled tasks: {", ".join([x.name for x in tasks])}'
    TelegramNotification().send(message)
    logger.info(message)

    while True:
        for task in tasks:
            if not task.should_be_checked():
                time.sleep(0.2)
                continue
            try:
                run = task.run()
                task.mark_checked()

                if not (AUTO_RECOVER and run and task.should_be_checked() and task.can_recover()):
                    time.sleep(0.2)
                    continue
                task.recover()
                task.mark_recovered()

            except Exception as error:
                logger.error(f'Error in task {task.name}: {traceback.format_exc()}')
                logger.error(error.__str__())

            time.sleep(0.2)

        TelegramNotification().flush()
        sys.stdout.flush()
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
