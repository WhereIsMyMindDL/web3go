from loguru import logger
import ccxt
import random

from .myaccount import Account
from help import retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data
from settings import binance_withdraw, amount, apiKey, secret, decimal_places

send_list = ''
class zkBridge(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)

    def binance_withdraw(self):
        global send_list
        amount_to_withdrawal = round(random.uniform(amount[0], amount[1]), decimal_places)
        exchange = ccxt.binance({
            'apiKey': apiKey,
            'secret': secret,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot'
            }
        })

        try:
            exchange.withdraw(
                code='BNB',
                amount=amount_to_withdrawal,
                address=self.address,
                tag=None,
                params={
                    "network": 'BSC'
                }
            )
            print(f'\n>>>[Binance] Вывел {amount_to_withdrawal} BNB ', flush=True)
            self.wait_balance(int(self.w3.to_wei(amount_to_withdrawal, 'ether') * 0.8), rpc='BSC')
            send_list += (f'\n{SUCCESS}Binance: Withdraw {amount_to_withdrawal} BNB')


        except Exception as error:
            print(f'\n>>>[Binance] Не удалось вывести {amount_to_withdrawal} BNB: {error} ', flush=True)


    @retry
    def bridge(self):
        global send_list

        value_wei = random.randint(500000000000000, 800000000000000)

        value_with_fee = int((value_wei + 1326000000000000))

        balance_eth = self.w3.from_wei(value_wei, 'ether')


        data = f'0x14d9e0960000000000000000000000000000000000000000000000000000000000000017{self.w3.to_bytes(int(value_wei)).hex().zfill(64)}000000000000000000000000{self.address[2:]}'
        tx_data = get_tx_data(self, to='0x51187757342914E7d94FFFD95cCCa4f440FE0E06', value=value_with_fee, data=data)

        logger.info(f'zkbridge: Bridge {"{:0.9f}".format(balance_eth)} BNB to opBNB')
        txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

        if txstatus == 1:
            logger.success(f'zkbridge: Bridge {"{:0.9f}".format(balance_eth)} BNB : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}zkbridge: Bridge {"{:0.4f}".format(balance_eth)} BNB to opBNB - [tx hash]({self.scan + tx_hash})')
            self.wait_balance(int(value_wei * 0.8), rpc='opBNB')


        else:
            logger.error(f'zkbridge: Bridge {"{:0.9f}".format(balance_eth)} BNB : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}zkbridge: Bridge {"{:0.4f}".format(balance_eth)} BNB to opBNB - failed')


    def main(self):
        global send_list
        send_list = ''
        if binance_withdraw:
            zkBridge.binance_withdraw(self)
        zkBridge.bridge(self)

        return send_list

