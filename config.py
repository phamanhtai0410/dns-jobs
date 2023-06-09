# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = os.getenv("DEBUG")
    PROJECT = "dns-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')

    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')

    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')
    AUTH_PRIVATE_KEY = os.getenv('AUTH_PRIVATE_KEY', '')
    TOKEN_EXPIRE_TIME = int(os.getenv('TOKEN_EXP_TIME', default='864000'))

    # Config celery worker
    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    BROKER_USE_SSL = True
    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.task_register_domain': {'queue': 'dns-domain-queue'},
        'worker.on_trade_nft': {'queue': 'dns-domain-queue'},
        'worker.on_transfer_nft': {'queue': 'dns-domain-queue'},
    }

    # Redis
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))

    # Blockchain
    ETH_RPC_URI = os.getenv('ETH_RPC_URI')
    CHAIN_ID = int(os.getenv('CHAIN_ID'))

    WALLET_IAPI = os.getenv('WALLET_IAPI')
    CONFIRM_BLOCK = 1

    TOP_LEVEL_DOMAIN = '.meme'

    SIGNATURE_EXPIRE_TIME = 60 * 60
    SIGNATURE_BUY_NFT_EXPIRE_TIME = 60 * 60
    BLOCKCHAIN_DECIMALS = {
        '0': 'wei',
        '3': 'kwei',
        '6': 'mwei',
        '9': 'gwei',
        '12': 'szabo',
        '15': 'finney',
        '18': 'ether'
    }

    ADDRESS0 = '0x0000000000000000000000000000000000000000'
    MARKETPLACE_CONTRACT = os.getenv('MARKETPLACE_CONTRACT')