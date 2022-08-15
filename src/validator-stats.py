#!/usr/bin/python3

'''
Reece Williams (Reecepbcups | PBCUPS Validator [$DIG]) | August 14th, 2022
- Twitter & Discord Integration + Endpoints

Install:
- pip install --no-cache-dir -r requirements.txt

Run:
- python validator-stats.py

Docker:
- docker build -t reecepbcups/validatorstats .
- docker run reecepbcups/validatorstats

*Get REST lcd's in chain.json from https://github.com/cosmos/chain-registry
'''

import requests
import schedule
import time
import json
import tweepy
import os

# from discord import Webhook, RequestsWebhookAdapter
from utils.notifications import discord_notification

from ChainApis import chainAPIs

HEADERS = {
    'accept': 'application/json', 
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

def main():
    print("Initial run...")
    runChecks()

    if USE_PYTHON_RUNNABLE: 
        # Can't use schedule bc its thread blocking = kuber thinks it dies
        prev = time.time()        
        while True:
            now = time.time()
            if now - prev > SCHEDULE_MINUTES*60:            
                prev = now
                print("Checks would be run here")
                runChecks()

# Don't touch below --------------------------------------------------

PREFIX = "COSMOSVALSTATS"
def getENV(path, default):    
    value = os.getenv(f"{PREFIX}_{path}", default)
    return value

def str2bool(v) -> bool: 
    return str(v).lower() in ("yes", "true", "t", "1")

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

    DEBUGGING = bool(getENV("DEBUGGING", False))

    USE_PYTHON_RUNNABLE = bool(getENV(f"SCHEDULER_USE_PYTHON_RUNNABLE", secrets["SCHEDULER"]["USE_PYTHON_RUNNABLE"]))
    SCHEDULE_MINUTES = int(getENV(f"SCHEDULER_IF_ABOVE_IS_TRUE_HOW_MANY_MINUTES_BETWEEN_CHECKS", secrets["SCHEDULER"]["IF_ABOVE_IS_TRUE_HOW_MANY_MINUTES_BETWEEN_CHECKS"]))

    OPERATOR_ADDRESSES = secrets['OPERATOR_ADDRESSES']
    _wallets = os.getenv(f"{PREFIX}_OPERATOR_ADDRESSES") # only works on local linmux docker run
    if _wallets is not None: # grabs from file, but if there is an env variable it uses that
        OPERATOR_ADDRESSES = dict(eval(_wallets))['OPERATOR_ADDRESSES']
        print("using" + _wallets + " from the env variable")
    print(OPERATOR_ADDRESSES)

    # loop through all os variables & print out keys for debugging
    for key in os.environ:
        if key.startswith(PREFIX):
            print(f"\tOUR KEYS: {key} = {os.getenv(key)}")

    discSecrets = secrets['DISCORD']
    IMAGE = os.getenv(f"{PREFIX}_DISCORD_IMAGE", discSecrets['IMAGE'])
    WEBHOOK_URL = os.getenv(f"{PREFIX}_DISCORD_WEBHOOK_URL", discSecrets['WEBHOOK_URL'])
    USERNAME = discSecrets['USERNAME']

    print(WEBHOOK_URL)


def simplifyBalances(balances: dict):
    '''
    After using getBalances(chain, wallet) function return -> dict:
    Reduces [{"denom": "ucraft","amount": "69908452"},{"denom": "uexp","amount": "1000100"}]
    To: {'ucraft':69908452, 'uexp':1000100}
    '''
    output = {}
    for balance in balances:
        denom = balance['denom']
        amount = balance['amount']

        if denom.startswith('ibc/'):
            continue # skip non native assets
        elif denom.startswith('gamm'):
            continue # skip osmo pools
        
        if denom.startswith('u'):
            output[denom[1::]] = int(amount) / 1_000_000
        elif denom.startswith('aevmos'): # bruh evmos u crazy
            output[denom[1::]] = int(amount) / 1_000_000_000_000_000_000
        else:
            output[denom] = int(amount)
            
    # print(chain, walletAddr, output)
    return dict(output)

# :NEW:
def reduceBalance(denom: str, amount: int) -> str:    
    # removes the u denom & div by 1mil. So ucraft 1000000 = craft 1
    if denom.startswith('u'):        
        fmtNum = "{:,}".format(round(int(amount) / 1_000_000, 2))
        return f"{fmtNum} {denom[1::]}"

    elif denom.startswith('aevmos'): # bruh evmos u crazy
        fmtNum = "{:,}".format(round(int(amount) / 1_000_000_000_000_000_000, 2))
        return f"{fmtNum} {denom[1::]}"

    else:        
        return f"{int(amount)} {denom}"

# :new:
def getChainsImage(chain):
    # gets the URL of the chain
    if len(IMAGE) > 0:
        return IMAGE

    url = chainAPIs[chain][-2]
    
    # check if url is a dict
    if isinstance(url, str) and "http" in url:
        return url
    if isinstance(url, dict):
        url = url['logo']

    print('image:', url)
    return IMAGE

def getValidatorStats(chain, walletAddr) -> dict:
    '''
    Returns a dict of information about a given validator
    https://api.cosmos.network/cosmos/staking/v1beta1/validators/cosmosvaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qkrka4zk
    '''

    queryEndpoint = chainAPIs[chain][0] + walletAddr

    # get a validators details
    r = requests.get(queryEndpoint, headers=HEADERS)
    if r.status_code != 200:
        print(f"\n(Error): {r.status_code} on {chainAPIs[chain][0]}")
        return {}
    validatorData = r.json()['validator']

    # get chain params
    params_url = f"{chainAPIs[chain][0].split('/cosmos/')[0]}/cosmos/staking/v1beta1/params"
    r = requests.get(params_url, headers=HEADERS)
    if r.status_code != 200:
        print(f"\n(Error): {r.status_code} on {chainAPIs[chain][0]}")
        return {}
    paramsData = r.json()['params']

    # ! IMPORTANT, this may take a while
    # get total # of unique delegators
    #  https://lcd-osmosis.blockapsis.com/cosmos/staking/v1beta1/validators/osmovaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qk5wjn0s/delegations?pagination.limit=10000
    try:
        # raise Exception("test")
        delegators_url = f"{chainAPIs[chain][0].split('/cosmos/')[0]}/cosmos/staking/v1beta1/validators/{walletAddr}/delegations?pagination.limit=10000"
        r = requests.get(delegators_url, headers=HEADERS)
        if r.status_code != 200:
            print(f"\n(Error): {r.status_code} on delegators_url: {delegators_url}")       
        uniqueDelegators = f"{len(r.json()['delegation_responses'])}"
    except:
        uniqueDelegators = "-1"


    return {
        "chain": chain,
        "operator_address": validatorData['operator_address'],
        "jailed": validatorData['jailed'], 
        "status": validatorData['status'], # BOND_STATUS_BONDED
        "bonded_utokens": f"{int(validatorData['tokens'])}", # then based on bond_denom, convert
        "bonded_tokens": reduceBalance(paramsData['bond_denom'], int(validatorData['tokens'])),
        "moniker": validatorData['description']['moniker'],
        "identity": validatorData['description']['identity'],
        "website": validatorData['description']['website'],
        "security_contact": validatorData['description']['security_contact'],
        "commission": validatorData['commission']['commission_rates']['rate'],
        "max_validators": paramsData['max_validators'],
        "bond_denom": paramsData['bond_denom'],        
        "unique_delegators": uniqueDelegators,        
    }
    
# stats = getValidatorStats("cosmos", "cosmosvaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qkrka4zk")
# print(stats)
# exit()

def postUpdate(chain, walletAddress):
    try:
        print(f"Getting update for {chain} - {walletAddress}")
        stats = getValidatorStats(chain, walletAddress)
        values = {
            "Chain": [chain.upper(), True],
            # "Address": [walletAddress, False],
            "Bonded Tokens": [stats['bonded_tokens'], True],
            "Commission": [f"{float(stats['commission'])*100}%", False],
            "Unique Delegators": [f"{stats['unique_delegators']}", False],
            # "Website": [stats['website'], False],
        }

        discord_notification(
            WEBHOOK_URL,
            "Oni Validator Stats",
            "",
            "D04045",        
            values,
            getChainsImage(chain),
            "The Oni Protectorate ⚛️\nValidator for the Cosmos. Friend to the Cosmonaut."
        )

    except Exception as err:
        print( str(err) + " OR Tweet failed due to being duplicate")


def runBalanceCheckForWallet(chain, wallet):
    # balances = getBalances(chain, wallet)
    # simplified = simplifyBalances(balances)
    # postUpdate(chain, wallet, simplified)
    pass

def runChecks():   
    print("Running checks...") 

    # Go through all wallets & ChainAPis matching. If the wallet starts with a ChainAPI keyname
    # check the balance of that wallet using the given LCD API
    checkedWallets = []
    for wallet in OPERATOR_ADDRESSES:
        for chain in chainAPIs.keys():
            if wallet.startswith(chain):
                checkedWallets.append(wallet)
                # runBalanceCheckForWallet(chain, wallet)
                postUpdate(chain, wallet)

    print(f"Wallets checked {time.ctime()}, waiting...")

    # Tell user which wallets were not checked due to no endpoints
    if len(checkedWallets) != len(OPERATOR_ADDRESSES):
        try:
            _temp = OPERATOR_ADDRESSES
            for wallet in checkedWallets:
                # _temp.remove(wallet)
                del _temp[wallet]
            print("\n(ERROR): Left over wallets (MAKE SURE TO ADD AN ENDPOINT TIO ChainApis.py): \n" + ',\n'.join(_temp.keys()))
        except Exception as err:
            print(str(err))
            print("Checked wallets: " + str(checkedWallets))



if __name__ == "__main__":   
    # postUpdate('cosmos', "cosmosvaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qkrka4zk")
    main()