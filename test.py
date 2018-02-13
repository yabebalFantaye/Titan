import os
import sys
import argparse
import time 
from time import sleep

from core import titan_main
from core.database import database
from strategies import poc_strategy

import logging

logger = logging.getLogger(__name__)

def arg_parser():
    info='''
    Bot to buy and sell cryptocurrency. 
    '''
    parser = argparse.ArgumentParser(description=info)
    
    parser.add_argument(
        "-r", "--real",
        dest="live_trading",
        action="store_const",
        const=True,
        default=False,
        help="Start Live Trading.")
    
    parser.add_argument(
        "-e","--exchange",
        dest="exchange",
        default="kraken",        
        help="The crypto exchange name.")
    
    parser.add_argument(
        "-b","--base",
        dest="basecurrency",
        default="BTC",        
        help="The base currency name.")

    parser.add_argument(
        "-q","--quote",
        dest="quotecurrency",
        default="USD",        
        help="The quote currency name.")

    parser.add_argument(
        "-c","--candle",
        dest="candleinterval",
        default="5m",        
        help="The candle interval.")
    

    parser.add_argument(
        "--fma",
        dest="fma",
        default=100,        
        help="The fast moving average time window.")

    parser.add_argument(
        "--sma",
        dest="sma",
        default=700,        
        help="The slow moving average time window.")

    parser.add_argument(
        "--balance",
        dest="balance",
        default=10,        
        help="The initial accunt balance for simulation.")
    
    return parser


def read_args():
    parser = arg_parser()
    args = parser.parse_args()
    return args

def basic_strategy():
    args = read_args()    
    user_exchange = args.exchange
    user_basecurrency = args.basecurrency
    user_quotecurrency = args.quotecurrency
    user_candleinterval = args.candleinterval
    user_sma = args.sma
    user_fma = args.fma
    user_balance = args.balance
    
    if not args.live_trading:
        simulate=True
        user_input = [user_exchange.lower(), user_basecurrency.upper(), user_quotecurrency.upper(),
                      user_candleinterval, simulate, int(user_sma), int(user_fma), int(user_balance)]
        
        titan_main.start_strategy(user_input)
    else:
        simulate=False        
        user_input = [user_exchange.lower(), user_basecurrency.upper(), user_quotecurrency.upper(),
                      user_candleinterval, simulate, int(user_sma), int(user_fma), int(user_balance)]
        
        strategy = poc_strategy.PocStrategy(user_input[3], user_input[0], user_input[1],
                                                user_input[2], user_input[4], user_input[6],
                                                user_input[5], user_input[7]) # 
        strategy.start()
        
        
if __name__ == '__main__':
    args = read_args()        
    print(args)
    basic_strategy()
