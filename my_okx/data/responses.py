########################################################################################################################
# CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # CHECK KEYS # C
########################################################################################################################

"""
401
{
    'msg': 'Invalid OK-ACCESS-KEY',
    'code': '50111'
}
"""

"""
401
{
    'msg': 'Request header OK-ACCESS-PASSPHRASE incorrect.',
    'code': '50105'
}
"""

"""
401
{
    'msg': 'Invalid Sign',
    'code': '50113'
}
"""

########################################################################################################################
# GET ACCOUNT BALANCE # GET ACCOUNT BALANCE # GET ACCOUNT BALANCE # GET ACCOUNT BALANCE # GET ACCOUNT BALANCE # GET ACC
########################################################################################################################

"""
{
    'code': '0',
    'data':
        [
            {
                'adjEq': '',
                'details':
                    [
                        {
                            'availBal': '10.52',
                            'availEq': '',
                            'cashBal': '10.52',
                            'ccy': 'USDT',
                            'crossLiab': '',
                            'disEq': '10.517896',
                            'eq': '10.52',
                            'eqUsd': '10.517896',
                            'fixedBal': '0',
                            'frozenBal': '0',
                            'interest': '',
                            'isoEq': '',
                            'isoLiab': '',
                            'isoUpl': '',
                            'liab': '',
                            'maxLoan': '',
                            'mgnRatio': '',
                            'notionalLever': '',
                            'ordFrozen': '0',
                            'spotInUseAmt': '',
                            'stgyEq': '0',
                            'twap': '0',
                            'uTime': '1687191463728',
                            'upl': '',
                            'uplLiab': ''
                        }
                        ...
                    ],
                'imr': '',
                'isoEq': '',
                'mgnRatio': '',
                'mmr': '',
                'notionalUsd': '',
                'ordFroz': '',
                'totalEq': '10.517896',
                'uTime': '1687192004687'
            }
        ],
    'msg': ''
}
"""

########################################################################################################################
# GET FUNDING BALANCE # GET FUNDING BALANCE # GET FUNDING BALANCE # GET FUNDING BALANCE # GET FUNDING BALANCE # GET FUND
########################################################################################################################

"""
{
    'code': '0',
    'data': 
        [
            {
                'availBal': '10',
                'bal': '10',
                'ccy': 'USDT',
                'frozenBal': '0'
            },
            {
                'availBal': '4.99500105',
                'bal': '4.99500105',
                'ccy': 'USDC',
                'frozenBal': '0'
            }
        ],
    'msg': ''
}
"""

########################################################################################################################
# GET NETWORKS # GET NETWORKS # GET NETWORKS # GET NETWORKS # GET NETWORKS # GET NETWORKS # GET NETWORKS # GET NETWORKS
########################################################################################################################

"""
[
    {
        'canDep': True,
        'canInternal': True,
        'canWd': True,
        'ccy': 'USDT',
        'chain': 'USDT-OKTC',
        'depQuotaFixed': '',
        'depQuoteDailyLayer2': '',
        'logoLink': 'https://static.coinall.ltd/cdn/oksupport/asset/currency/icon/usdt20230419113051.png',
        'mainNet': False,
        'maxFee': '0.4',
        'maxFeeForCtAddr': '0.4',
        'maxWd': '2679040',
        'minDep': '0.00000001',
        'minDepArrivalConfirm': '2',
        'minFee': '0.2',
        'minFeeForCtAddr': '0.2',
        'minWd': '1',
        'minWdUnlockConfirm': '4',
        'name': 'Tether',
        'needTag': False,
        'usedDepQuotaFixed': '',
        'usedWdQuota': '0',
        'wdQuota': '10000000',
        'wdTickSz': '8'
    },
    {
        'canDep': True,
        'canInternal': True,
        'canWd': True,
        'ccy': 'USDT',
        'chain': 'USDT-ERC20',
        'depQuotaFixed': '',
        'depQuoteDailyLayer2': '',
        'logoLink': 'https://static.coinall.ltd/cdn/oksupport/asset/currency/icon/usdt20230419113051.png',
        'mainNet': False,
        'maxFee': '7.6323728',
        'maxFeeForCtAddr': '7.6323728',
        'maxWd': '5358080',
        'minDep': '0.00000001',
        'minDepArrivalConfirm': '64',
        'minFee': '3.8161864',
        'minFeeForCtAddr': '3.8161864',
        'minWd': '2',
        'minWdUnlockConfirm': '96',
        'name': 'Tether',
        'needTag': False,
        'usedDepQuotaFixed': '',
        'usedWdQuota': '0',
        'wdQuota': '10000000',
        'wdTickSz': '8'
    },
    ...  
 ]
"""

########################################################################################################################
# POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST WITHDRAWAL ON CHAIN # POST WITHD
########################################################################################################################

'''
{
    'code': '58207',
    'data': [],
    'msg': 'Withdrawal address is not whitelisted for verification exemption'
}
'''

'''
{
    'code': '0',
    'data': 
        [
            {
                'amt': '0.1',
                'ccy': 'USDT',
                'chain': 'USDT-Arbitrum One',
                'clientId': '',
                'wdId': '90942945'
            }
        ],
    'msg': ''
}
'''

########################################################################################################################
# GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL HISTORY # GET WITHDRAWAL # G
########################################################################################################################

'''
{
    'code': '0',
    'data': 
        [
            {
                'chain': 'GLMR-Moonbeam',
                'areaCodeFrom': '7',
                'clientId': '',
                'fee': '0.01',
                'amt': '2.27272727',
                'txId': '0x0f871d59079b2911cda466f55260a1c51c200a3a6553f68b58f40a799f1b000c',
                'areaCodeTo': '',
                'ccy': 'GLMR',
                'from': '9264551638',
                'to': '0xAC9efC702947d825d167B2163d80a3f2897B7c0d',
                'state': '2',
                'nonTradableAsset': False,
                'ts': '1708092918000',
                'wdId': '153560764',
                'feeCcy': 'GLMR'
            }
        ],
    'msg': ''
}
'''

########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
