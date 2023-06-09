# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import traceback
import sentry_sdk
from pydash import get
from pymongo import ReturnDocument

from config import Config
from lib.enums.tx_type import TxType
from lib.logger import debug
from lib.utils import dt_utcnow
from models import TxLogsModel, NsNftModel
from worker import worker


@worker.task(name="worker.on_transfer_nft", rate_limit='1000/s')
def on_transfer_nft(event):
    try:
        debug(event)
        _from = get(event, 'args.from').lower()
        if _from == Config.ADDRESS0:
            debug('--- Transfer from address(0) ---')
            return 'DONE - on_transfer_nft'
        _tx_hash = get(event, 'transactionHash', '').lower()
        _contract = get(event, 'address').lower()
        _owner = get(event, 'args.to').lower()
        _token_id = get(event, 'args.tokenId')
        _tx = TxLogsModel.update_one(
            filter={
                'tx_hash': _tx_hash,
                'contract': _contract,
                'token_id': _token_id
            },
            obj={
                'tx_type': TxType.TRANSFER,
                'contract': _contract,
                'event': json.dumps(event),
                'block_number': get(event, 'blockNumber'),
                "updated_time": dt_utcnow(),
                'updated_by': 'dns-api:tasks:transfer'

            },
            upsert=True,
            return_document=ReturnDocument.BEFORE
        )
        if _tx:
            debug(f"--- Transfer tx {_tx_hash} already exist ---")
            return 'DONE - on_transfer_nft'

        _update = {
            'updated_time': dt_utcnow(),
            'updated_by': 'dns-api:tasks:trade',
            'buy_deadline': 0,
            'owner': _owner
        }
        _filter = {
            'contract': _contract,
            'token_id': _token_id
        }

        NsNftModel.update_one(
            filter=_filter,
            obj=_update,
            upsert=False
        )

        return 'DONE - on_transfer_nft'

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return "FAIL - on_transfer_nft"
