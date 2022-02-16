import asyncio
import json
import urllib.request as ur
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand

# import keep_alive

discord_token = os.environ['discord_token']
etherscan_api_key = os.environ['etherscan_api_key']

bot = commands.Bot(
    command_prefix="k!",  # bot prefix
    case_insensitive=True,  # case-sensitive
    intents=discord.Intents.all(),
    help_command=None
)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("Bot ready!")
    while True:
        url1 = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + etherscan_api_key  # api url

        site1 = ur.urlopen(url1)
        page1 = site1.read()
        contents1 = page1.decode()
        data1 = json.loads(contents1)

        ethusd = data1['result']['ethusd']
        #####
        url2 = 'https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=' + etherscan_api_key  # api url

        site2 = ur.urlopen(url2)
        page2 = site2.read()
        contents2 = page2.decode()
        data2 = json.loads(contents2)

        SafeGasPrice = data2['result']['SafeGasPrice']
        ProposeGasPrice = data2['result']['ProposeGasPrice']
        FastGasPrice = data2['result']['FastGasPrice']

        presence_ctx1 = 'Ξ ' + ethusd
        presence_ctx2 = '🚀' + FastGasPrice + '🚗' + ProposeGasPrice + '🚲' + SafeGasPrice

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence_ctx1))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=presence_ctx2))
        await asyncio.sleep(10)


# Load Cog
extensions = [
    'cogs.account',
    'cogs.help',
    'cogs.invite',
    'cogs.ping',
    'cogs.project_history',
    'cogs.project_nft',
    'cogs.project_realtime',
    'cogs.project_rarity',
    'cogs.txn'
]

if __name__ == '__main__':
    for extension in extensions:
        bot.load_extension(extension)

# keep_alive.keep_alive()
bot.run(discord_token)
