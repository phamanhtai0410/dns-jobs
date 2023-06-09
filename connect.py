# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import asyncio

import motor
from flask_pymongo import PyMongo
import motor.motor_asyncio
from rediscluster import RedisCluster
from web3 import Web3
from blockchain import Blockchain
from config import Config

from lib import Chains


class InterfaceAsync:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
        self.client.get_io_loop = asyncio.get_event_loop
        self.db = self.client.core


connect_db = PyMongo()

redis_cluster = RedisCluster(
    startup_nodes=Config.REDIS_CLUSTER,
    decode_responses=True,
    skip_full_coverage_check=True
)

web3_providers = {
    # ETHEREUM
    "1": Blockchain(Chains.ETHEREUM, Web3.HTTPProvider(Config.ETH_RPC_URI, request_kwargs={'timeout': 60})),
    # GOERLI
    "5": Blockchain(Chains.ETHEREUM, Web3.HTTPProvider(Config.ETH_RPC_URI, request_kwargs={'timeout': 60})),
}

from lib import HTTPSecurity

security = HTTPSecurity(redis=redis_cluster, auth_address=Config.AUTH_ADDRESS)
