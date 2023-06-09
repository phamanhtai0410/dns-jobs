# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import pydash as py_
from ens import BaseENS
from eth_utils import to_wei, from_wei
import bson.json_util

from connect import redis_cluster
from lib import get_dsn_erc721_token_id, get_dsn_erc1155_token_id
from lib.logger import debug
from worker import worker
from config import Config

from models import TxLogsModel, NsNftModel

@worker.task(name='worker.task_register_domain', rate_limit='1000/s')
def task_register_domain(event: str):
    try:
        print(event)
        _tx_hash = py_.get(event, 'transactionHash')
        _blocknumber = py_.get(event, 'blockNumber')
        _contract = py_.get(event, 'address').lower()
        _args = py_.get(event, 'args')

        _domain_name = py_.get(_args, 'name')

        _erc721_token_id = get_dsn_erc721_token_id(_domain_name)

        _erc1155_token_id = get_dsn_erc1155_token_id(f'{_domain_name}{Config.TOP_LEVEL_DOMAIN}')

        _ns_nft = NsNftModel.find_one({
            'token_id': _erc1155_token_id
        })

        if _ns_nft:
            return 'ERROR - dns existed'

        _domain_data = {
            'token_id': _erc1155_token_id,
            'erc721_token_id': _erc721_token_id,
            'domain_name': f'{_domain_name}{Config.TOP_LEVEL_DOMAIN}',
            'owner': py_.get(_args, 'owner').lower(),
            'expires': py_.get(_args, 'expires'),
            'base_cost': '{0:f}'.format((from_wei(py_.get(_args, 'baseCost'), 'ether'))),
            'contract': _contract,
            'chain_id': py_.get(event, 'chain'),
            'created_by': 'tasks:domain:task_register_domain'
        }


        NsNftModel.insert_one(_domain_data)

        TxLogsModel.insert_one({
            'tx_hash': _tx_hash,
            'token_id': _erc1155_token_id,
            'block_number': _blocknumber,
            'contract': _contract,
            'tx_type': 'NameRegistered',
            'event': bson.json_util.dumps(event),
            'chain_id': py_.get(event, 'chain'),
            'created_by': 'tasks:domain:task_register_domain'
        })

        return 'DONE - task_register_domain'
    except Exception as e:
        debug(f'ERROR - task_register_domain: {e}')
        return 'ERROR - task_register_domain'
