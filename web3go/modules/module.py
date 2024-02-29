import time
from loguru import logger
from pyuseragents import random as random_ua
from requests import Session
from datetime import datetime
from eth_account.messages import encode_defunct
import requests
import datetime

from .myaccount import Account
from help import retry, sign_and_send_transaction, SUCCESS, FAILED, get_tx_data


send_list = ''
class module(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.session = Session()
        self.session.headers['user-agent'] = random_ua()
        self.proxy = proxy
        if self.proxy != None:
            self.session.proxies.update({'http': f"http://{self.proxy}"})

    @retry
    def mint_pass(self):
        global send_list
        send_list = ''

        data = f'0x40d097c3000000000000000000000000{self.address[2:]}'
        tx_data = get_tx_data(self, to='0xa4Aff9170C34c0e38Fed74409F5742617d9E80dc', data=data)
        logger.info(f'Web3go: Mint pass')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction=tx_data)

        if txstatus == 1:
            logger.success(f'Web3go: Mint pass : {self.scan + tx_hash}')
            send_list += (f'\n{SUCCESS}Web3go: Mint pass - [tx hash]({self.scan + tx_hash})')

        else:
            logger.error(f'Web3go: Mint pass : {self.scan + tx_hash}')
            send_list += (f'\n{FAILED}Web3go: Mint pass - failed')
        return send_list


    def login(self):
        self.session.headers.update({
            'Accept': '*/*',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Origin': 'https://reiki.web3go.xyz',
            'Referer': 'https://reiki.web3go.xyz/aiweb/home',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'app-site-code': 'home',
            'content-type': 'application/json',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-app-channel': 'DIN',
            'x-public-api': 'public-api',
        })

        json_data = {
            'address': self.address,
        }

        response = self.session.post('https://reiki.web3go.xyz/api/account/web3/web3_nonce',
                                     headers=self.session.headers, json=json_data).json()
        nonce = response['nonce']
        challenge = response['challenge']

        output_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        msg = f"reiki.web3go.xyz wants you to sign in with your Ethereum account:\n{self.address}\n\n{challenge}\n\nURI: https://reiki.web3go.xyz\nVersion: 1\nChain ID: 56\nNonce: {nonce}\nIssued At: {output_date}"
        message = encode_defunct(text=msg)
        text_signature = self.w3.eth.account.sign_message(message, private_key=self.private_key)

        signature_value = text_signature.signature.hex()
        json_data = {
            'address': self.address,
            'nonce': nonce,
            'challenge': '{"msg":"' + msg.replace('\n', '\\n') + '"}',
            'signature': signature_value,
        }

        response = requests.post(
            'https://reiki.web3go.xyz/api/account/web3/web3_challenge',
            json=json_data,
        ).json()
        token = response['extra']['token']
        self.session.headers["Authorization"] = f"Bearer {token}"

    @retry
    def proof_wallet(self):
        module.login(self)

        start_data = int(datetime.datetime.utcnow().strftime("%Y%m%d"))
        response = self.session.get(url=f"https://reiki.web3go.xyz/api/checkin/points/his?start={start_data}&end={start_data + 1}").json()

        params = {
            'day': datetime.datetime.now().strftime("%Y-%m-%d"),
        }

        response_check_in = self.session.put('https://reiki.web3go.xyz/api/checkin', params=params).json()

        response = self.session.get('https://reiki.web3go.xyz/api/profile').json()

        if response_check_in:
            time.sleep(1)
            logger.success(f'Daily check in success | Available golds: {response["goldLeafCount"]}')
            return 1
        else:
            logger.error(f'Daily check failed | Available golds: {response["goldLeafCount"]}')
            return 0

    @retry
    def get_quiz(self):
        module.login(self)

        quiz1 = {
            'b9778bc8-9068-4ec7-963e-4f1316f7e7bb': 'A',
            '886818e4-2cd2-4b33-a92a-3926d8085ccc': 'B',
            '08c2cdd6-7f7f-412b-90ce-fba5317aec67': 'B',
            '13f3d40e-fa6f-4183-b75e-54c3364b055a': 'A',
            '34c7ed18-072d-4807-b9a8-fc399b56e45d': 'A',
        }

        quiz2 = {
            'e3add053-86fe-41aa-ba49-3e36c31fc72b': 'C',
            '1ad19c42-7348-407a-a0a0-f9d4d5cbdedf': 'D',
            '880a4595-3f55-4b28-9f6d-c010a4322a5b': 'D',
            '267c7827-97f5-4b61-bf4d-ccec208aad3b': 'D',
            'fa303d33-7bb0-4c40-ac47-a9983ee48b81': 'C',
        }

        quiz3 = {
            '2473c67d-2c29-4edb-b798-68714ca67379': 'A',
            '4adf6472-a8ce-4dc1-b5a4-274e6a21a83b': 'D',
            'a5aa3e7e-a554-4add-a3df-7563b8061bc5': 'C',
            '74066c03-c641-4c48-883a-a94b7d5b41fd': 'B',
            '148f45c4-9504-44a2-954a-dffc42f33597': 'C',
        }

        quiz4 = {
            'ececb607-0706-471a-90bc-cb5b31bb11dc': 'A',
            '916f7bc4-6dde-4dc5-98fd-c7ded26a70d1': 'B',
            '0c5a947a-c28c-4cfe-97a6-40f3aaf951c9': 'B',
            '02763ec2-dcda-48e2-8b0d-8485f3ee55c7': 'A',
            '6b2952fb-3087-498c-8746-649a4ea6106a': 'A',
        }

        quiz5 = {
            '3ac99871-27ed-4898-a3da-b91c77b0f884': 'A',
            '9a422518-32f3-41b2-b969-848f825d24b1': 'D',
            'b2570533-fec7-48ee-a057-37e15595fcd8': 'A',
            '9b55c40f-88ad-475c-b118-092dfb817d66': 'B',
            '7050c01c-fc6e-4879-b2eb-3ef010424c5d': 'D',
        }

        quiz6 = {
            'c9af4601-ea03-49c8-82e2-95f55074e703': self.address,
            'e2e51c43-1472-4b8d-aa64-1a8379ba96ac': 'B',
            '149c7a36-ee93-4199-b1e4-411ed9b0be6d': 'B',
            'b94c1708-363d-4995-9cde-caccf47315e7': 'A',
            'e403fe5e-f1b5-43c0-a3c1-571aeaf712e8': 'B',
        }


        try:
            response = self.session.post('https://reiki.web3go.xyz/ai/console/api/app/aibot/nft/sync').json()
            response = self.session.get('https://reiki.web3go.xyz/api/nft/sync').json()

            params = {
                'type': 'recent',
            }

            response = self.session.get('https://reiki.web3go.xyz/api/profile').json()
            response = self.session.get('https://reiki.web3go.xyz/api/gift', params=params).json()
            response = self.session.post(f'https://reiki.web3go.xyz/api/gift/open/{response[0]["id"]}').json()

            logger.success(f'Успешная активация пасса')
        except:
            logger.info(f'Пасс уже активирован')

        logger.info(f'Начинаю проходить квизы...')
        quizz = [quiz1, quiz2, quiz3, quiz4, quiz5, quiz6]
        for quiz in quizz:
            for key in quiz:
                time.sleep(1)
                json_data = {'answers': [quiz[key], ], }
                response = self.session.post(f'https://reiki.web3go.xyz/api/quiz/{key}/answer', json=json_data).json()
                # logger.success(response['message'])
        time.sleep(5)
        response = self.session.get('https://reiki.web3go.xyz/api/profile').json()
        logger.success(f'Успешно прошел 6/6 | Available golds: {response["goldLeafCount"]}')
