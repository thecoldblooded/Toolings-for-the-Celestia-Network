import time

import requests

from chain_stuck import elapsed_to_string
from custom_logging import logger
from tasks import Task, minutes
from constants import Emoji, CHAIN_ENDPOINT
from utils import run_command


def rpc_call(url, method, headers=None, params=[]):
    try:
        response = requests.post(
            url, headers=headers, json={'jsonrpc': '2.0', 'id': 1, 'method': 'das.SamplingStats', 'params': params}, timeout=60
        ).json()
        return response['result']
    except Exception as error:
        logger.error('Send RPC request failed!')
        logger.error(error.__str__())
        return None


class Chain:
    ENDPOINT = ''

    def __init__(self):
        if CHAIN_ENDPOINT:
            self.ENDPOINT = CHAIN_ENDPOINT

    def rpc_call(self, method, headers=None, params=[]):
        return rpc_call(self.ENDPOINT, method, headers, params)

    def get_version(self):
        raise Exception('Abstract get_version()')

    def get_height(self):
        raise Exception('Abstract get_height()')

    def get_block_hash(self):
        raise Exception('Abstract get_block_hash()')

    def get_network_height(self):
        raise Exception('Abstract get_network_height()')


class CheckSamplesHeight(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'CheckSamplesHeight'
        self.since = None
        self.stuck_block_count = 0

    def run(self):
        if not self.chain.is_synching():
            block_height = self.chain.get_network_height()
            block_height_sampled = self.chain.get_samples_height()

            if self.since is None:
                self.since = time.time()
                return False

            if block_height > block_height_sampled:
                self.stuck_block_count += 1
                elapsed = elapsed_to_string(self.since)
                return self.notify(
                    f'Is not sampling new headers, last block sampled is {block_height_sampled}, current block header is {block_height} ({elapsed}) {Emoji.STUCK}')  # noqa

            if self.stuck_block_count > 0:
                elapsed = elapsed_to_string(self.since)
                self.notify(f'Is back sampling new headers (after {elapsed}) {Emoji.SYNC_OK}')

            self.since = time.time()
            self.stuck_block_count = 0
        return False


class NodeIsSynching(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'NodeIsSynching'
        self.previous = None
        self.since = None
        self.stuck_block_count = 0

    def run(self):
        block_height = int(self.chain.get_height())

        if self.previous is None:
            self.previous = block_height
            self.since = time.time()
            return False

        network_head = self.chain.get_network_head()
        network_height = int(network_head['header']['height'])
        if block_height > self.previous and abs(block_height - network_height) > 100:
            self.stuck_block_count += 1
            return self.notify(
                f'chain is synching, last block stored is {block_height}, current network height is {network_height} {Emoji.SLOW}')  # noqa

        if self.stuck_block_count > 0:
            elapsed = elapsed_to_string(self.since)
            self.notify(f'chain synched in {elapsed} {Emoji.SYNC_OK}')

        self.previous = block_height
        self.since = time.time()
        self.stuck_block_count = 0
        return False


class P2PChecking(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'P2PChecking'
        self.check_every = minutes(10)
        self.notify_every = minutes(10)

    def run(self):
        bandwidth_stats = self.chain.get_bandwidth_stats()
        return self.notify(f'Bandwidth: {bandwidth_stats} {Emoji.BANDWIDTH}')


class StateChecking(Task):
    def __init__(self, chain):
        super().__init__(chain)
        self.name = 'StateChecking'
        self.check_every = minutes(10)
        self.notify_every = minutes(10)

    def run(self):
        state_amount = self.chain.get_state_amount()
        return self.notify(f'State amount: {state_amount} {Emoji.STATE_AMOUNT}')


class CelestiaNode(Chain):
    ENDPOINT = 'http://localhost:26658/'
    AUTH_TOKEN = None
    CUSTOM_TASKS = [
        CheckSamplesHeight,
        NodeIsSynching,
        P2PChecking,
        StateChecking,
    ]

    def rpc_call(self, method, headers=None, params=[]):
        if not self.ENDPOINT:
            self.ENDPOINT = CHAIN_ENDPOINT
        if not self.AUTH_TOKEN:
            self.AUTH_TOKEN = run_command("celestia light auth admin --p2p.network blockspacerace")
        headers = {'Authorization': f'Bearer {self.AUTH_TOKEN}'}
        return super().rpc_call(method, headers, params)

    def get_version(self):
        ver = run_command("celestia version | head -n 1")
        return ver.split(" ")[-1]

    def get_height(self):
        return self.rpc_call('header.LocalHead')['header']['height']

    def get_network_height(self):
        return int(self.rpc_call('header.NetworkHead')['header']['height'])

    def get_block_hash(self):
        return self.rpc_call('header.NetworkHead')['header']['last_block_id']['hash']

    def get_peer_count(self):
        return len(self.rpc_call('p2p.Peers'))

    def is_synching(self):
        return not self.rpc_call('das.SamplingStats')['catch_up_done']

    def get_samples_height(self):
        return self.rpc_call('das.SamplingStats')['head_of_sampled_chain']

    def get_bandwidth_stats(self):
        return self.rpc_call('p2p.BandwidthStats')

    def get_state_amount(self):
        return self.rpc_call('state.Balance')['amount']
