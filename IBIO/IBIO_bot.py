import discord
from random import randint, choice
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import os

TOKEN = "ODM0Nzc1NzE0MDExOTM4ODY2.YIFzdw.xtrzUpaBwMEn4tvzWqxyCXpzjIQ"
ibio = commands.Bot(command_prefix='!')
const_month = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


@ibio.event
async def on():
    print('Запуск')


@ibio.command()
async def ready(ctx):
    await ctx.message.channel.send('```IBIO``` подключён.')
    await ctx.message.author.voice.channel.connect(reconnect=True)


@ibio.command()
async def IBIO_help(ctx):
    await ctx.message.channel.send('```IBIO комманды:\n'
                                   'ready - вкл/выкл бот\n'
                                   'уточни ("исчесление времени") - говорит время```')


@ibio.command()
async def уточни(ctx, args):
    arg = (''.join((''.join(args.split('('))).split(')'))).lower()
    day = int((str((datetime.datetime.now().date())).split('-'))[2])
    month = const_month[int((str((datetime.datetime.now().date())).split('-'))[1])]
    year = int((str((datetime.datetime.now().date())).split('-'))[0])
    if arg == 'дата':
        await ctx.message.channel.send(f'```{day} {month} {year} год.```')
    elif arg == 'время':
        await ctx.message.channel.send(f'```{datetime.datetime.now().hour}:{datetime.datetime.now().minute}```')


@ibio.command()
async def play(ctx, url : str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        pass
    await ctx.message.channel.send('Подождите...\n'
                                   '```!!!НЕТ ОЧЕРЕДИ, ВАШЕЙ МУЗЫКИ НЕ БУДЕТ ПОСЛЕ ТЕКУЩЕЙ!!!``` ')
    voice = get(ibio.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'[log] {name}, ok'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1


ibio.run(TOKEN)
