import datetime
import os
import time

from blockchainetl.logging_utils import logging_basic_config
from ethereumetl.service.eth_service import EthService, BlockTimestampGraph
from ethereumetl.providers.auto import get_provider_from_uri
from ethereumetl.utils import check_classic_provider_uri
from ethereumetl.web3_utils import build_web3
from ethereumetl.jobs.export_blocks_job import ExportBlocksJob
from ethereumetl.jobs.exporters.blocks_and_transactions_item_exporter import blocks_and_transactions_item_exporter
from ethereumetl.thread_local_proxy import ThreadLocalProxy
from ethereumetl.service.graph_operations import OutOfBoundsError

logging_basic_config()

this_hour = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, second=0, minute=0)
hour_ago = this_hour - datetime.timedelta(hours=1)
this_hour_ts = this_hour.timestamp()
hour_ago_ts = hour_ago.timestamp()

provider_uri = os.environ.get('PROVIDER_URL', 'file:///home/ubuntu/node/geth.ipc')

def get_block_range_for_timestamps(provider_uri, start_timestamp, end_timestamp, chain='binance'):
    """Outputs start and end blocks for given timestamps."""
    original_provider_uri = provider_uri
    provider_uri = check_classic_provider_uri(chain, provider_uri)
    provider = get_provider_from_uri(provider_uri)
    web3 = build_web3(provider)
    eth_service = EthService(web3)
    try:
        return eth_service.get_block_range_for_timestamps(start_timestamp, end_timestamp)
    except OutOfBoundsError:
        # OutOfBoundsError is raised if yet there is no block for endtime timestamp
        # Typically that issue is gone within 3 seconds
        time.sleep(1)
        get_block_range_for_timestamps(original_provider_uri, start_timestamp, end_timestamp, chain='binance')


def export_blocks_and_transactions(start_block, end_block, batch_size, provider_uri, max_workers, blocks_output,
                                   transactions_output, chain='binance'):
    """Exports blocks and transactions."""
    provider_uri = check_classic_provider_uri(chain, provider_uri)
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri, batch=True)),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter(blocks_output, transactions_output),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None)
    job.run()

if __name__ == '__main__':
    start_block, end_block = get_block_range_for_timestamps(provider_uri, hour_ago_ts, this_hour_ts)
    _date, this_hour = str(this_hour).replace('+00:00', '').split(' ')
    _date, hour_ago = str(hour_ago).replace('+00:00', '').split(' ')
    export_blocks_and_transactions(
        start_block=start_block,
        end_block=end_block,
        batch_size=end_block - start_block,
        provider_uri=provider_uri,
        max_workers=5,
        blocks_output='/tmp/dummy.csv',
        transactions_output=f'data/extracted/{_date}/{hour_ago}-{this_hour}.csv'
    )
