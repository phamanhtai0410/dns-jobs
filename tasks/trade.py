# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import traceback
import sentry_sdk
from bson import ObjectId
from pydash import get
from pymongo import ReturnDocument

from lib.enums.tx_type import TxType
from lib.logger import debug
from lib.utils import dt_utcnow
from models import TxLogsModel, OrdersModel
from worker import worker


@worker.task(name="worker.on_trade_nft", rate_limit='1000/s')
def on_trade_nft(event):
    try:
        debug(event)
        _order_id = get(event, 'args.orderID')
        _from_to = get(event, 'args.fromTo', [])
        _from = get(_from_to, '[0]')
        _to = get(_from_to, '[1]')
        _tx_hash = get(event, 'transactionHash', '').lower()
        _tx = TxLogsModel.update_one(
            filter={
                'tx_hash': _tx_hash,
                'tx_type': TxType.TRADE
            },
            obj={
                'tx_type': TxType.TRADE,
                'event': json.dumps(event),
                'block_number': get(event, 'blockNumber'),
                "updated_time": dt_utcnow(),
                'updated_by': 'dns-api:tasks:trade'
            },
            upsert=True,
            return_document=ReturnDocument.BEFORE
        )

        if _tx:
            debug(f"--- Trade tx {_tx_hash} already exist ---")
            return 'DONE - on_trade_nft'

        _sell_order = OrdersModel.find_one(filter={"order_id": _order_id})

        if not _sell_order:
            debug(f"--- Sell order id {_order_id} not found ---")
            return 'DONE - on_trade_nft'

        OrdersModel.insert_one({
            'chain': get(_sell_order, 'chain'),
            'token_id': get(_sell_order, 'token_id'),
            'order_id': get(_sell_order, 'order_id'),
            'price': get(_sell_order, 'price'),
            'nft_id': ObjectId(get(_sell_order, 'nft_id')),
            'sender': ObjectId(get(_sell_order, 'sender')),
            'receiver': ObjectId(get(_sell_order, 'receiver')),
            'action': 'BUY',
            'data': get(_sell_order, 'data'),
            'updated_time': dt_utcnow(),
            'created_time': dt_utcnow(),
            'updated_by': '',
            'created_by': 'dns-api:tasks:on_trade_nft',
        })

        return 'DONE - on_trade_nft'

    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return "FAIL - on_trade_nft"
