import discord
from discord.ext import tasks
from discord import FFmpegPCMAudio
import time
import datetime
import asyncio
import random

CLIENT_TOKEN = ''
SOUND_PATH = './sounds/tacoBell.wav'
GUILD_ID = 0
DEFAULT_CHANNEL_ID = 0
IGNORED_CHANNELS = [0, 0]

 
client = discord.Client()

def random_channel():
    voiceChannels = []
    channel_id = DEFAULT_CHANNEL_ID
    for voiceChannel in client.get_guild(GUILD_ID).voice_channels:
        if len(voiceChannel.voice_states) != 0:
            if voiceChannel.id not in IGNORED_CHANNELS:
                voiceChannels.append(voiceChannel)
    if len(voiceChannels) != 0:
        rando = random.randint(0, len(voiceChannels)-1)
        channel_id = voiceChannels[rando].id
    return channel_id

async def chime_once(voice, sound):
    source = FFmpegPCMAudio(sound)
    voice.play(source)
    while(voice.is_playing()): await asyncio.sleep(0.5)

async def play(channel_id):
    voiceChannel = client.get_channel(channel_id)
    hours = int(datetime.datetime.now().strftime("%I:%M")[:2])
    voice = await voiceChannel.connect()
    for hour in range(hours):
        await chime_once(voice, SOUND_PATH)
    if voice and voice.is_connected():
        await voice.disconnect()

@tasks.loop(seconds = 1)
async def myLoop():
    bits = datetime.datetime.now().strftime("%I:%M:%S").split(":")
    minute = int(bits[1])
    second = int(bits[2])
    if minute == 13 and second == 30:
        await play(random_channel())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

myLoop.start()
client.run(CLIENT_TOKEN)
