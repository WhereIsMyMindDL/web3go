import time
from loguru import logger
import random
import datetime

from help import send_message, sleeping_between_wallets, intro, outro, send_list, SUCCESS
from settings import bot_status, bot_id, bot_token, shuffle, mode
from modules.myaccount import Account
from modules.module import module

day_now = int(datetime.datetime.now(datetime.timezone.utc).strftime("%d"))

def main():
    with open('proxies.txt', 'r') as file:  # login:password@ip:port в файл proxy.txt
        proxies = [row.strip() for row in file]
    with open('wallets.txt', 'r') as file:
        wallets = [row.strip() for row in file]

    intro(wallets)
    count_wallets = len(wallets)

    if len(proxies) == 0:
        proxies = [None] * len(wallets)

    if len(proxies) != len(wallets):
        logger.error('Proxies count doesn\'t match wallets count. Add proxies or leave proxies file empty')
        return

    data = [(wallets[i], proxies[i]) for i in range(len(wallets))]

    if shuffle:
        random.shuffle(data)

    def proccessing():
        global day_now
        success_wallets = 0

        for idx, (wallet, proxy) in enumerate(data, start=1):
            private_key = wallet

            account = Account(idx, private_key, proxy, 'BSC')

            print(f'{idx}/{count_wallets} : {account.address}\n')
            try:
                if mode == 1:
                    send_list.append(f'{account.id}/{count_wallets} : [{account.address}]({"https://debank.com/profile/" + account.address})')
                    send_list.append(module(account.id, account.private_key, account.proxy, 'BSC').mint_pass())
                elif mode == 2:
                    success_wallets += module(account.id, account.private_key, account.proxy, 'BSC').proof_wallet()
                elif mode == 3:
                    module(account.id, account.private_key, account.proxy, 'BSC').get_quiz()
            except Exception as e:
                logger.error(f'{idx}/{count_wallets} Failed: {str(e)}')


            if bot_status == True:
                if account.id == count_wallets:
                    if mode == 2:
                        send_list.append(f'{SUCCESS}*Web3Go Claimer*\n\nToday success claim points: {success_wallets}/{count_wallets}')
                    send_list.append(f'\nSubscribe: https://t.me/CryptoMindYep')
                if len(send_list) != 0:
                    send_message(bot_token, bot_id, send_list)
            send_list.clear()

            if idx != count_wallets:
                sleeping_between_wallets()
                print()
        if mode == 2:
            print()
            time.sleep(0.3)
            logger.info(f'Waiting next day...')
            time.sleep(0.3)
            print()
            while int(datetime.datetime.now(datetime.timezone.utc).strftime("%d")) == day_now:
                time.sleep(600)
            day_now = int(datetime.datetime.now(datetime.timezone.utc).strftime("%d"))
            proccessing()
    proccessing()
    outro()
main()