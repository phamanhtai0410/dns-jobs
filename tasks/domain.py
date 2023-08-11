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

from exceptions.nfts import UserNotOwnNftEx 
from models import TxLogsModel, NsNftModel, HistoryPointModel, TotalPointModel, DefaultPointModel, MintLogsModel

@worker.task(name='worker.task_register_domain', rate_limit='1000/s')
def task_register_domain(event: str):
    try:
        print(event)
        _tx_hash = py_.get(event, 'transactionHash')
        _blocknumber = py_.get(event, 'blockNumber')
        _contract = Config.NAME_WRAPPER_CONTRACT.lower()
        _args = py_.get(event, 'args')

        _domain_name = py_.get(_args, 'name')

        _erc721_token_id = get_dsn_erc721_token_id(_domain_name)

        _erc1155_token_id = get_dsn_erc1155_token_id(f'{_domain_name}{Config.TOP_LEVEL_DOMAIN}')

        _ns_nft = NsNftModel.find_one({
            'token_id': _erc1155_token_id
        })
        # if _ns_nft:
            # return 'ERROR - dns existed'

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

         # add point to user who mint Domain 
        _mint = MintLogsModel.find_one({
            'user_address':py_.get(_args, 'owner').lower(),
            'domain_name':f'{_domain_name}{Config.TOP_LEVEL_DOMAIN}',
        })
        if _mint:
            print(py_.get(_args, 'owner').lower())
            print(_mint)
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            obj = TotalPointModel.find_one({
                'user_address':py_.get(_args, 'owner').lower(),
            })
            _rule = DefaultPointModel.find_one({})
            # print(_rule)
            claim = 0
            if _mint['letter'] == 3:
                claim = _rule['three']
            elif _mint['letter'] == 4:
                claim = _rule['four']
            else:
                claim = _rule['five']
            if obj:        
                TotalPointModel.update_one({
                    'user_address':py_.get(_args, 'owner').lower(),
                },
                {
                    'total_point':obj['total_point'] + claim,
                    'updated_by':'dns-job' 
                })
            else:
                TotalPointModel.insert_one({
                    'user_address':py_.get(_args, 'owner').lower(),
                    'referral':0,
                    'total_point':claim,
                    'created_by': 'dns-api:services:POINTsService:new_user',
                    'updated_by': 'dns-api:services:POINTsService:update_point'
                })    
            HistoryPointModel.insert_one({
                'user_address': py_.get(_args, 'owner').lower(),
                'point_type':'mint',
                'point': claim,
                'created_by': 'dns-api:services:POINTsService:mint_point',
            })      
            # add point to user who sent the referral link
            _referral_address = _mint['ref_address']
            obj2 = TotalPointModel.find_one({
                'user_address':_referral_address
            })
            minted = NsNftModel.find_one({
                'owner':_referral_address,
            })
            print("****************************************************")
            print(minted)
            if minted:
                bonus = 10
                if not obj2:
                    _referral = 0
                    _totalpoint = 0
                    TotalPointModel.insert_one({
                    'user_address':_referral_address,
                    'referral':0,
                    'total_point':0,
                    'created_by': 'dns-api:services:POINTsService:new_user',
                    'updated_by': 'dns-api:services:POINTsService:update_point'
                    })
                else:
                    _referral = obj2['referral']
                    _totalpoint = obj2['total_point']

                if _referral >= _rule['level4']:
                    bonus = _rule['point4']
                elif _referral >= _rule['level3']:
                    bonus = _rule['point3']
                elif _referral >= _rule['level2']:
                    bonus = _rule['point2']
                elif _referral >= _rule['level1']:
                    bonus = _rule['point1']           
                bonus = claim*(bonus/100)
                claim = round(bonus)
                _new = MintLogsModel.find({
                    'user_address': py_.get(_args, 'owner').lower(),
                    'ref_address':_referral_address
                })
                print(_referral)
                count = 0
                for _ in _new:
                    count += 1

                if count == 1:
                    _referral += 1
                print(count)
                print(_referral)
   

                TotalPointModel.update_one({
                    'user_address':_referral_address,
                },
                {
                    'referral':_referral,
                    'total_point':_totalpoint + claim,
                    'updated_by':'dns-job'
                })
                HistoryPointModel.insert_one({
                    'user_address': _referral_address,
                    'point_type':'referral',
                    'point': claim,
                    'created_by': 'dns-api:services:POINTsService:referral_point',
                })  

        return 'DONE - task_register_domain'
    except Exception as e:
        debug(f'ERROR - task_register_domain: {e}')
        return 'ERROR - task_register_domain'
