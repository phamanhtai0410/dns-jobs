# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get
from connect import redis_cluster
from lib import ethereum, bsc, arbitrum, base_testnet, set_name_services
from lib.logger import debug
from services.ens import ENSServices, SpaceIDServices, BaseNameServices
from worker import worker

SUPPORT_CHAIN = [ethereum, bsc, arbitrum, base_testnet]


@worker.task(name='worker.task_set_user_name_services', rate_limit='1000/s')
def task_set_user_name_services(address: str):
    try:
        _ens_name = ENSServices.get_ens_name_from_eth_address(address=address)
        _bnb_domain = SpaceIDServices.get_domain_from_address(tld='bnb', address=address)
        _arb_domain = SpaceIDServices.get_domain_from_address(tld='arb1', address=address)
        _base_domain = BaseNameServices.get_domain_from_address(address=address)

        _domain_names = [_ens_name, _bnb_domain, _arb_domain, _base_domain]
        _result = []
        for index, chain in enumerate(SUPPORT_CHAIN):
            _item = {
                'chain_id': get(chain, 'id'),
                'chain_name': get(chain, 'name'),
                'list_domain': _domain_names[index],
            }
            _result.append(_item)

        set_name_services(redis_cluster=redis_cluster, address=address, data=_result)

        return 'DONE - task_set_user_name_services'
    except Exception as e:
        debug(f'ERROR - task_set_user_name_services: {e}')
        set_name_services(redis_cluster=redis_cluster, address=address, data=[])
        return 'ERROR - task_set_user_name_services'
