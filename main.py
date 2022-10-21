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


intents = discord.Intents.all()
# intents.typing = True
# intents.presences = True

bot = commands.AutoShardedBot(intents=intents, command_prefix='$')

class MapCheck:
    def __init__(self, map, channel):
        self.map = map
        self.channel = channel


class PlayersChecker:
    def __init__(self, message):
        self.message = message


@bot.event
async def on_ready():
    
    print('Bot is ready')



@bot.command(name='asd')
async def asd(ctx):
    async def button_callback(interaction):
        embed = discord.Embed(title='ArkGame66Players', color=discord.Color.green())
        resp = requests.get('https://arkgame66.ru/servers_status').json()
        print(resp['servers'])
        servers_value = ''
        players_value = ''

        for i in resp['servers']:
            circle = ':green_circle:' if i['status'] else ':red_circle'
            servers_value += f'{circle} [{i["id"]}] **{i["name"]}** __{i["players"]}/{i["maxplayers"]}__\n'

        for i in resp['players']:
            players_value += f'{i["name"]} {i["server"]}\n'
        embed.add_field(name='Servers', value=servers_value, inline=False)
        embed.add_field(name=f'Players {len(resp["players"])}', value=f"```{players_value}```")
        print(resp['servers'])
        await interaction.response.edit_message(embed=embed)

    button = Button(custom_id='button1', label='WOW button!', style=discord.ButtonStyle.green)
    view = View()
    view.add_item(button)
    button.callback = button_callback
    players_message = await ctx.channel.send(view=view)
    players_checker_message = PlayersChecker(players_message.id)


# async def edit_message(ctx, embed):
    
#     resp = requests.get('https://arkgame66.ru/servers_status').json()
#     print(resp['servers'])
#     servers_value = ''
#     players_value = ''

#     for i in resp['servers']:
#         circle = ':green_circle:' if i['status'] else ':red_circle'
#         servers_value += f'{circle} [{i["id"]}] **{i["name"]}** __{i["players"]}/{i["maxplayers"]}__\n'

#     for i in resp['players']:
#         players_value += f'{i["name"]} {i["server"]}\n'
#     embed.add_field(name='Servers', value=servers_value, inline=False)
#     embed.add_field(name=f'Players {len(resp["players"])}', value=f"```{players_value}```")
#     return embed


@bot.command(name='check')
async def check_map(ctx, *args):
    map = ' '.join(args)
    mapcheck = MapCheck(map, ctx.channel.id)
    bot.loop.create_task(enemy_check(ctx, mapcheck))


async def enemy_check(ctx, mapcheck):
    print('abobboboboobboba')
    while True:
        enemies = ''
        resp = requests.get('https://arkgame66.ru/servers_status').json()
        # print(resp['players'])
        for i in resp['players']:
            try:
                asd = i['name'].split(' (')[1][:-1]
            except:
                asd = ''
            print(mapcheck.map.strip() + '   |||   ' + i['server'])
            if asd == 'Hustler' or asd == 'How to not Solo' and i['server'] == mapcheck.map.strip():
                print(i)
                enemies += f'Enemy {i["name"]} on the map {i["server"]}\n'
        channel = bot.get_channel(mapcheck.channel)
        await channel.send(enemies)
        del enemies      
        await asyncio.sleep(10)



# token = os.environ['TOKEN']

if __name__ == '__main__':
    token = 'MTAxNzE0OTcwODAwMDU1OTExNA.GFQsWC.pmSjrluhY5brWNfpWNXsrhRrxKCbCk0cIhH498'
    bot.run(token)