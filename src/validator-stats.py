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

import time
import json
import os

from utils.notifications import discord_notification, discord_graph_notification

from pyibc_api import get_chain, REST_ENDPOINTS, CHAIN_APIS, get_all_chains # just for the keys
from pyibc_chain.validators import get_validator_stats

import stats_and_image

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

# check if secrets.json exists
if not os.path.isfile('secrets.json'):
    print("\n\nsecrets.json not found. Please follow the instructions in the readme...")
    print("(( cp secrets.example.json secrets.json ))")
    exit()

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

    DEBUGGING = bool(getENV("DEBUGGING", False))

    USE_PYTHON_RUNNABLE = bool(getENV(f"SCHEDULER_USE_PYTHON_RUNNABLE", secrets["SCHEDULER"]["USE_PYTHON_RUNNABLE"]))
    SCHEDULE_MINUTES = int(getENV(f"SCHEDULER_IF_ABOVE_IS_TRUE_HOW_MANY_MINUTES_BETWEEN_CHECKS", secrets["SCHEDULER"]["IF_ABOVE_IS_TRUE_HOW_MANY_MINUTES_BETWEEN_CHECKS"]))

    OPERATOR_ADDRESSES = dict(secrets['OPERATOR_ADDRESSES'])
    _wallets = os.getenv(f"{PREFIX}_OPERATOR_ADDRESSES") # only works on local linmux docker run
    if _wallets is not None: # grabs from file, but if there is an env variable it uses that
        # NOT TESTED
        OPERATOR_ADDRESSES = dict(eval(_wallets))['OPERATOR_ADDRESSES']
        print("using" + _wallets + " from the env variable")
    # print(OPERATOR_ADDRESSES)

    # check if EXTRA_NOTES key is in secrets.json
    EXTRA_NOTES = {}
    if 'EXTRA_NOTES' in secrets:
        EXTRA_NOTES = dict(secrets['EXTRA_NOTES'])


    IMAGES_URL = os.getenv(f"{PREFIX}_DISCORD_IMAGES_URL", secrets['IMAGES_URL'])    
    if IMAGES_URL.endswith('/'): IMAGES_URL = IMAGES_URL[:-1]

    LINE_COLOR = os.getenv(f"{PREFIX}_GRAPH_COLORS_LINE", secrets['GRAPH_COLORS']['LINE'])  
    CHART_BACKGROUND = os.getenv(f"{PREFIX}_GRAPH_COLORS_CHART_BACKGROUND", secrets['GRAPH_COLORS']['CHART_BACKGROUND'])
    MAIN_BACKGROUND = os.getenv(f"{PREFIX}_GRAPH_COLORS_MAIN_BACKGROUND", secrets['GRAPH_COLORS']['MAIN_BACKGROUND'])

    # loop through all os variables & print out keys for debugging
    for key in os.environ:
        if key.startswith(PREFIX):
            print(f"\tOUR KEYS: {key} = {os.getenv(key)}")

    discSecrets = secrets['DISCORD']
    IMAGE = os.getenv(f"{PREFIX}_DISCORD_IMAGE", discSecrets['IMAGE'])
    WEBHOOK_URL = os.getenv(f"{PREFIX}_DISCORD_WEBHOOK_URL", discSecrets['WEBHOOK_URL'])
    USERNAME = discSecrets['USERNAME']
    COLOR = discSecrets['COLOR']
    FOOTER = discSecrets['FOOTER']
    # print(WEBHOOK_URL)

def getChainsImage(chain):
    # gets the URL of the chain
    if len(IMAGE) > 0:
        return IMAGE

    return get_chain(chain).get('logo', '')

# stops discord CDN from caching, used in the image path
# year, month, day

now = time.strftime("%Y_%b_%d_%H_%M_%S", time.localtime())

def postUpdate(chain, walletAddress, graph=""):
    print(f"Getting update for {chain} - {walletAddress}")
    
    if len(graph) > 0:
        print("API URL provided, getting graphs")
        img_stats = stats_and_image.get_stats(graph)

        COLORS = {
            'LINE': LINE_COLOR,
            'CHART_BACKGROUND': CHART_BACKGROUND,
            'MAIN_BACKGROUND': MAIN_BACKGROUND
        }

        stats_and_image.make_image(chain, img_stats, "votingPower", now, title="Stake Secured", yAxis=chain, xAxis="Date", colors=COLORS)
        stats_and_image.make_image(chain, img_stats, "uniqueDelegates", now, title="Unique Delegators", yAxis="Delegators", xAxis="Date", colors=COLORS)

        stats = get_validator_stats(
            chain=chain, 
            rest_url=get_chain(chain)['rest_root'], 
            operator_address=walletAddress, 
            include_number_of_unique_delegations=False
        )
        values = {
            "Chain": [chain.upper(), True],            
            "Bonded Tokens": [stats['bonded_tokens'], True],
            "Commission": [f"{float(stats['commission'])*100}%", False],    
            "Ranking": [f"#{stats['validator_ranking']} / {stats['max_validators']}", False]  
            # "Unique Delegators": [f"{stats['unique_delegators']}", False], # make include_number_of_unique_delegations if you want this
        }

        if walletAddress in EXTRA_NOTES.keys() and len(EXTRA_NOTES[walletAddress])>0: # adds extra thing to the embed if the wallet has extra notes enabled
            values["Note"] = [EXTRA_NOTES[walletAddress], False]

        discord_graph_notification(
            webhook=WEBHOOK_URL, 
            title=USERNAME, 
            description="", 
            color=COLOR, 
            values=values, 
            graph_image_links=[
                f"{IMAGES_URL}/{chain}_votingPower_{now}.png",
                f"{IMAGES_URL}/{chain}_uniqueDelegates_{now}.png",
            ],            
            thumbnail=getChainsImage(chain),
            footer=FOOTER,
        )
 
    else:
        try:
            stats = get_validator_stats(
                chain=chain, 
                rest_url=get_chain(chain)['rest_root'], 
                operator_address=walletAddress, 
                include_number_of_unique_delegations=True
            )
            values = {
                "Chain": [chain.upper(), True],            
                "Bonded Tokens": [stats['bonded_tokens'], True],
                "Commission": [f"{float(stats['commission'])*100}%", False],
                "Ranking": [f"#{stats['validator_ranking']} / {stats['max_validators']}", False],
                "Unique Delegators": [f"{stats['unique_delegators']}", False],          
            }

            if walletAddress in EXTRA_NOTES.keys() and len(EXTRA_NOTES[walletAddress])>0: # adds extra thing to the embed if the wallet has extra notes enabled
                values["Note"] = [EXTRA_NOTES[walletAddress], False]

            discord_notification(
                WEBHOOK_URL,
                USERNAME,
                "",
                COLOR,        
                values,
                getChainsImage(chain),
                FOOTER
            )

        except Exception as err:
            print( "ERROR: ", str(err))

def runChecks():   
    print("Running checks...")

    # delete all png images from inside of the images folder
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(parent_dir, 'images')    
    # print(images_dir)
    # delete all pnf files in the images folder
    print("Deleting old png files from the last run")
    files_len = len(os.listdir(images_dir))
    for file in os.listdir(images_dir):
        if file.endswith(".png"):
            os.remove(os.path.join(images_dir, file))
    print(f"Removed {files_len} png files")

    # Go through all wallets & ChainAPis matching. If the wallet starts with a ChainAPI keyname
    # check the balance of that wallet using the given LCD API
    print("Generating new charts...")
    checkedWallets = []
    for wallet in OPERATOR_ADDRESSES.keys():
        for chain in get_all_chains():
            if str(wallet).startswith(chain):
                postUpdate(chain, wallet, graph=OPERATOR_ADDRESSES[wallet])
                checkedWallets.append(wallet)                        
    print(f"Operator wallets checked {time.ctime()}, waiting...")

    # Tell user which wallets were not checked due to no endpoints
    if len(checkedWallets) != len(OPERATOR_ADDRESSES):
        try:
            _temp = OPERATOR_ADDRESSES
            for wallet in checkedWallets:                
                del _temp[wallet]
            print("\n(ERROR): Left over wallets (MAKE SURE TO ADD AN ENDPOINT TO ChainApis.py): \n" + ',\n'.join(_temp.keys()))

        except Exception as err:
            print(str(err))
            print("Checked wallets: " + str(checkedWallets))

if __name__ == "__main__":   
    # postUpdate('cosmos', "cosmosvaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qkrka4zk")
    main()