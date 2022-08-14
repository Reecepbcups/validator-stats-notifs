'''
Dict of chains in the following format:

{
    "ticker": [
        "LCD endpoints for validator stats",
        {
            "ping": "https://ping.pub/ticker/gov/",
            "mintscan": "https://mintscan.io/ticker/proposals/",
        },
        "@twitter"
    ]
}

From: cosmos-balance-bot, replacedx

curl -X GET "https://api.cosmos.network/cosmos/staking/v1beta1/validators/cosmosvaloper16s96n9k9zztdgjy8q4qcxp4hn7ww98qkrka4zk" -H "accept: application/json"
'''

# /cosmos/staking/v1beta1/validators/<address>

chainAPIs = {
    "dig": [
        "https://api-1-dig.notional.ventures/cosmos/staking/v1beta1/validators/",
        {
            "ping": 'https://ping.pub/dig/gov',
        },
        "@dig_chain"
        ],
    'juno': [
        'https://lcd-juno.itastakers.com/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/juno/gov',
            "mintscan": 'https://www.mintscan.io/juno/proposals',
        },
        "@JunoNetwork"
        ],
    'huahua': [
        'https://api.chihuahua.wtf/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/chihuahua/gov',
            "mintscan": 'https://www.mintscan.io/chihuahua/proposals',
        },
        "@ChihuahuaChain"
        ],
    'osmo': [
        'https://lcd-osmosis.blockapsis.com/cosmos/staking/v1beta1/validators/',
        {
            # "ping": 'https://ping.pub/osmosis/gov',
            "mintscan": 'https://www.mintscan.io/osmosis/proposals',
        },
        "https://info.osmosis.zone/static/media/logo.551f5780.png",
        '@osmosiszone'
        ],
    'cosmos': [
        'https://rest.cosmos.directory/cosmoshub/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/cosmos/gov',
            "mintscan": 'https://www.mintscan.io/cosmos/proposals',
        },
        "https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/images/atom.png",
        "@cosmos"
        ],
    'akt': [
        'https://akash.api.ping.pub/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/akash-network/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
        },
        '@akashnet_'
        ],
    'stars': [
        "https://rest.cosmos.directory/stargaze/cosmos/staking/v1beta1/validators/",
        {
            "ping": 'https://ping.pub/stargaze/gov',
            # so hacked together here for validator-stats
            "logo": 'https://raw.githubusercontent.com/cosmos/chain-registry/master/stargaze/images/stars'
        },
        '@StargazeZone'
        ],
    'kava': [
        'https://api.data.kava.io/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/kava/gov',
            "mintscan": 'https://www.mintscan.io/kava/proposals',
        },        
        '@kava_platform'
        ],
    'like': [
        'https://mainnet-node.like.co/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/likecoin/gov',
        },
        '@likecoin'
        ],
    'xprt': [
        'https://rest.core.persistence.one/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/persistence/gov',
            "mintscan": 'https://www.mintscan.io/persistence/proposals',
        },        
        '@PersistenceOne'
        ],
    'comdex': [
        'https://rest.comdex.one/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/comdex/gov',
            "mintscan": 'https://www.mintscan.io/comdex/proposals',
        },       
        "https://raw.githubusercontent.com/cosmos/chain-registry/master/comdex/images/cmdx.png", 
        '@ComdexOfficial'
        ],
    "bcna": [ 
        'https://lcd.bitcanna.io/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/bitcanna/gov',
            "mintscan": 'https://www.mintscan.io/bitcanna/proposals',
        },        
        '@BitCannaGlobal'
        ],
    "btsg": [ 
        'https://lcd-bitsong.itastakers.com/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/bitsong/gov',
            "mintscan": 'https://www.mintscan.io/bitsong/proposals',
        },        
        '@BitSongOfficial'
        ],
    "band": [
        'https://laozi1.bandchain.org/api/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/band-protocol/gov',
            "mintscan": 'https://www.mintscan.io/akash/proposals',
        },        
        '@BandProtocol'
        ],
    "boot": [ # Bostrom
        'https://lcd.bostrom.cybernode.ai/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/bostrom/gov',
        },        
        ''
        ],
    "cheqd": [ 
        'https://api.cheqd.net/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/cheqd/gov',
        },        
        '@cheqd_io'
        ],
    "cro": [  
        'https://mainnet.crypto.org:1317/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/crypto-com-chain/gov',
            "mintscan": 'https://www.mintscan.io/crypto-org/proposals',
        },        
        '@cryptocom'
        ],
    "evmos": [  
        'https://rest.bd.evmos.org:1317/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/evmos/gov',
            "mintscan": 'https://www.mintscan.io/evmos/proposals',
        },
        "https://raw.githubusercontent.com/cosmos/chain-registry/master/evmos/images/evmos.png"
        '@EvmosOrg'
        ],
    "fetch": [
        'https://rest-fetchhub.fetch.ai/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/fetchhub/gov',
            "mintscan": 'https://www.mintscan.io/fetchai/proposals',
        },        
        '@Fetch_ai'
        ],
    "grav": [  
        'https://gravitychain.io:1317/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/gravity-bridge/gov',
            "mintscan": 'https://www.mintscan.io/gravity-bridge/proposals',
        },        
        '@gravity_bridge'
        ],
    "inj": [  
        'https://public.lcd.injective.network/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/injective/gov',
            "mintscan": 'https://www.mintscan.io/injective/proposals',
        },        
        '@InjectiveLabs'
        ],
    "iris": [  
        'https://lcd-iris.keplr.app/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/iris-network/gov',
            "mintscan": 'https://www.mintscan.io/iris/proposals',
        },        
        '@irisnetwork'
        ],
    'iov': [ #Starname
        "https://lcd-iov.keplr.app/cosmos/staking/v1beta1/validators/",
        {
            "ping": 'https://ping.pub/starname/gov',
            "mintscan": 'https://www.mintscan.io/starname/proposals',
        },        
        '@starname_me'
        ],
    "lum": [  
        'https://node0.mainnet.lum.network/rest/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/lum-network/gov',
            "mintscan": 'https://www.mintscan.io/lum/proposals',
        },        
        '@lum_network'
        ],
    "regen": [  
        'https://regen.stakesystems.io/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/regen/gov',
            "mintscan": 'https://www.mintscan.io/regen/proposals',
        },        
        '@regen_network'
        ],
    "hash": [  
        'https://api.provenance.io/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/provenance/gov',
        },        
        '@provenancefdn'
        ],
    "secret": [  
        'https://api.scrt.network/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/secret/gov',
            "mintscan": 'https://www.mintscan.io/secret/proposals',
        },        
        '@SecretNetwork'
        ],
    "sent": [  
        'https://lcd-sentinel.keplr.app/cosmos/staking/v1beta1/validators/',        
        {
            "ping": 'https://ping.pub/sentinel/gov',
            "mintscan": 'https://www.mintscan.io/sentinel/proposals',
        },        
        '@Sentinel_co'
        ],
    "sif": [  
        'https://api.sifchain.finance:443/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/sifchain/gov',
            "mintscan": 'https://www.mintscan.io/sifchain/proposals',
        },        
        "@sifchain"
        ],
    "terra": [  
        'https://blockdaemon-terra-lcd.api.bdnodes.net:1317/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/terra-luna/gov',
        },        
        "@terra_money"
        ],
    "umee": [  
        'https://api.blue.main.network.umee.cc/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://ping.pub/umee/gov',
            "mintscan": 'https://www.mintscan.io/umee/proposals',
        },        
        "@Umee_CrossChain"
        ],
    "kuji": [  
        'https://kujira-api.polkachu.com/cosmos/staking/v1beta1/validators/',
        {
            "ping": 'https://explorer.chaintools.tech/kujira/gov',
        },
        "https://raw.githubusercontent.com/cosmos/chain-registry/master/kujira/images/kujira-chain-logo.png",
        "@TeamKujira"
        ],
    "craft": [ 
        'http://65.108.125.182:1317/cosmos/staking/v1beta1/validators/',
    ]
}