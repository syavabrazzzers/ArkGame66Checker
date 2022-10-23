import datetime
from urllib import response
import discord
import os
import time
import requests
import json
import asyncio
import threading
from discord.ext import commands, tasks
from discord.ui import Button, View

print('hello dodik')


# intents = discord.Intents.all()
# intents.typing = True
# intents.presences = True


bot = commands.Bot(command_prefix='$')

class MapCheck:
    def __init__(self, map, channel, active):
        self.map = map
        self.channel = channel
        self.active = active


class PlayersChecker:
    def __init__(self, message):
        self.message = message


@bot.event
async def on_ready():
    
    print('Bot is ready')


# @bot.event
# async def on_message(message):
#     print(message.content)
#     print(message)


@bot.command(name='monitor', description='Create monitoring message')
async def monitor(ctx):
    message = await ctx.channel.send(embed=await create_embed())
    while True:
        await asyncio.sleep(5)
        await message.edit(embed=await create_embed())

    # button = Button(custom_id='button1', label='Update', style=discord.ButtonStyle.green)
    # view = View()
    # view.add_item(button)
    #
    # players_message = await ctx.channel.send(view=view)
    # players_checker_message = PlayersChecker(players_message.id)
    # button.callback = button_callback
    # print(players_checker_message.message)


async def create_embed():
    embed = discord.Embed(title='ArkGame66Info', color=discord.Color.green())
    resp = await get_server_info()
    servers_value = ''
    map = 'MAP              '
    player = 'PLAYER                    '
    players_value = map + player + '\n'

    for i in resp['servers']:
        circle = ':green_circle:' if i['status'] else ':red_circle'
        servers_value += f'{circle} [{i["id"]}] **{i["name"]}** __{i["players"]}/{i["maxplayers"]}__\n'

    for i in resp['players']:
        map_name = i['server'][:len(map)] if len(i['server']) > len(map) else (i['server'] + ' '*(len(map)-len(i['server'])))
        # print(map_name)
        player_name = f"{i['name']} ({i['tribe']})"
        players_value += (map_name + (player_name[:len(player)] if len(player_name) > len(player) else player_name) + '\n')
    embed.add_field(name='Servers', value=servers_value, inline=False)
    embed.add_field(name=f'Players {len(resp["players"])}', value=f"```{players_value}```", inline=True)
    embed.set_footer(text=f"Last update: {datetime.datetime.now().strftime('%H:%M:%S')}")
    return embed


maps_for_check = []
@bot.command(name='check', description='Check enemy on the map')
async def check_map(ctx, *args):
    map = args[0] if len(args) <= 2 else f'{args[0]} {args[1]}'
    mapcheck = MapCheck(map, ctx.channel.id, True)
    maps_for_check.append(mapcheck)
    try:
        enemy_for_check = int(ctx.message.content[-1])
    except:
        enemy_for_check = 3
    enemy = []
    channel = bot.get_channel(mapcheck.channel)
    while mapcheck.active:
        resp = requests.get('https://arkgame66.ru/servers_status').json()
        for i in resp['players']:
            if i['tribe'] != 'DRF' and i['server'] == mapcheck.map:
                enemy.append(f'{i["name"]} ({i["tribe"]})')
        if len(enemy) >= enemy_for_check:
            embed = discord.Embed(title='ArkGame66Info', color=discord.Color.red())
            message = ''
            for i in enemy:
                message += f'{i}\n'
            embed.add_field(name=f'Enemies ({len(enemy)})', value=message)
            await channel.send(embed=embed, content='')
        enemy.clear()
        await asyncio.sleep(60)


@bot.command(name='stop', description='Stop checking enemy on the map')
async def stop_check(ctx):
    for i in maps_for_check:
        if i.channel == ctx.channel.id:
            i.active = False


async def get_server_info():
    return requests.get('https://arkgame66.ru/servers_status').json()


async def enemy_check(ctx, mapcheck):
    print(f'Map: {mapcheck.map}\nChannel: {mapcheck.channel}')
    enemy = []
    channel = bot.get_channel(mapcheck.channel)
    print(int(ctx.message.content[-1]) or 3)
    print(int(ctx.message.content[-1]))
    while mapcheck.active:
        resp = requests.get('https://arkgame66.ru/servers_status').json()
        for i in resp['players']:
            if i['tribe'] != 'DRF' and i['server'] == mapcheck.map:
                enemy.append(f'{i["name"]} ({i["tribe"]})')
        if len(enemy) >= (int(ctx.message.content[-1]) or 3):
            embed = discord.Embed(title='ArkGame66Info', color=discord.Color.red())
            message = ''
            for i in enemy:
                message += f'{i}\n'

            embed.add_field(name=f'Enemies ({len(enemy)})', value=message)
            await channel.send(embed=embed, content='')
            enemy.clear()
        await asyncio.sleep(10)



# token = os.environ['TOKEN']

if __name__ == '__main__':
    token = os.environ['TOKEN']
    bot.run(token)
