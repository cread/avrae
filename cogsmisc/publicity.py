'''
Created on Dec 29, 2016

@author: andrew
'''
import aiohttp
import json
import credentials


DISCORD_BOTS_API = 'https://bots.discord.pw/api'

class Publicity:
    '''
    Sends updates to bot repos.
    '''
    
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        
    def __unload(self):
        # pray it closes
        self.bot.loop.create_task(self.session.close())

    async def update(self):

        payload = json.dumps({
            'server_count': len(self.bot.servers)
        })

        headers = {
            'authorization': credentials.discord_bots_key,
            'content-type': 'application/json'
        }

        url = '{0}/bots/{1.user.id}/stats'.format(DISCORD_BOTS_API, self.bot)
        async with self.session.post(url, data=payload, headers=headers) as resp:
            print('DBots statistics returned {0.status} for {1}'.format(resp, payload))

    async def on_server_join(self, server):
        await self.update()

    async def on_server_remove(self, server):
        await self.update()

    async def on_ready(self):
        await self.update()