# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['OrdersModel', 'SignatureLogModel']

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel

NFTContractsModel = DaoModel(col=connect_db.db.nft_contracts, redis=redis_cluster)
CryptoCurrenciesModel = DaoModel(col=connect_db.db.crypto_currencies, redis=redis_cluster)

OrdersModel = DaoModel(col=connect_db.db.orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

NsNftModel = DaoModel(col=connect_db.db.ns_nfts, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
TxLogsModel = DaoModel(col=connect_db.db.tx_logs, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

DevMintOrdersModel = DaoModel(col=connect_db.db.dev_mint_orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
SignatureLogModel = DaoModel(col=connect_db.db.signature_log, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

TotalPointModel = DaoModel(col=connect_db.db.total_points, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

HistoryPointModel = DaoModel(col=connect_db.db.history_points, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

DefaultPointModel = DaoModel(col=connect_db.db.default_points, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

MintLogsModel = DaoModel(col=connect_db.db.mint_logs, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)




