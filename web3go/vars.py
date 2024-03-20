import json

INVOLVED_CHAINS = ['Ethereum']

RPC = {
    'Ethereum': 'https://rpc.ankr.com/eth',
    'Optimism': 'https://rpc.ankr.com/optimism',
    'zkfair': 'https://rpc.zkfair.io',
    'BSC': 'https://rpc.ankr.com/bsc',
    'Gnosis': '',
    'Polygon': '',
    'Fantom': '',
    'Arbitrum': 'https://rpc.ankr.com/arbitrum',
    'Avalanche': '',
    'zkSync': 'https://1rpc.io/zksync2-era',
    'zkEVM': 'https://rpc.ankr.com/polygon_zkevm',
    'Zora': '',
    'Scroll': 'https://1rpc.io/scroll',
    'nova': 'https://arbitrum-nova.publicnode.com',
    'Linea': 'https://1rpc.io/linea',
    'Manta': 'https://1rpc.io/manta',
    'Base': 'https://base.llamarpc.com',
    'opBNB': 'https://opbnb.publicnode.com',
}

SCANS = {
    'Ethereum': 'https://etherscan.io/tx/',
    'Optimism': 'https://optimistic.etherscan.io/tx/',
    'BSC': 'https://bscscan.com/tx/',
    'Gnosis': 'https://gnosisscan.io/tx/',
    'Polygon': 'https://polygonscan.com/tx/',
    'Fantom': 'https://ftmscan.com/tx/',
    'Arbitrum': 'https://arbiscan.io/tx/',
    'Avalanche': 'https://snowtrace.io/tx/',
    'zkSync': 'https://explorer.zksync.io/tx/',
    'zkEVM': 'https://zkevm.polygonscan.com/tx/',
    'Zora': 'https://explorer.zora.energy/tx/',
    'Scroll': 'https://scrollscan.com/tx/',
    'Linea': 'https://lineascan.build/tx/',
    'nova': 'https://nova.arbiscan.io/tx/',
    'zkfair': 'https://scan.zkfair.io/tx/',
    'Manta': 'https://pacific-explorer.manta.network/tx/',
    'Base': 'https://basescan.org/tx/',
    'opBNB': 'https://opbnbscan.com/tx/',
}

CHAIN_IDS = {
    'Ethereum': 1,
    'Optimism': 10,
    'BSC': 56,
    'Gnosis': 100,
    'Polygon': 137,
    'Fantom': 250,
    'Arbitrum': 42161,
    'Avalanche': 43114,
    'zkSync': 324,
    'zkEVM': 1101,
    'Zora': 7777777,
    'Scroll': 534352,
    'nova': 42170,
    'Linea': 59144,
    'zkfair': 42766,
    'Manta': 169,
    'Base': 8453,
    'opBNB': 204,
}

CHAIN_NAMES = {
    1: 'Ethereum',
    10: 'Optimism',
    56: 'BSC',
    100: 'Gnosis',
    137: 'Polygon',
    250: 'Fantom',
    42161: 'Arbitrum',
    43114: 'Avalanche',
    1313161554: 'Aurora',
    324: 'zkSync',
    1101: 'zkEVM',
    7777777: 'Zora',
    534352: 'Scroll',
    42170: 'nova',
    59144: 'Linea',
    42766: 'zkfair',
    169: 'Manta',
    8453: 'Base',
    204: 'opBNB',
}

EIP1559_CHAINS = ['Ethereum', 'Zora', 'Optimism', 'Manta', 'opBNB']

NATIVE_TOKEN_ADDRESS = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

NATIVE_DECIMALS = 18
