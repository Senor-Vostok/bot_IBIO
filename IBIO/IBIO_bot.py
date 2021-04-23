import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import os

TOKEN = "ODM0Nzc1NzE0MDExOTM4ODY2.YIFzdw.amHT-daMEDuLRhQIxaxwMw09mkc"
ibio = commands.Bot(command_prefix='!')
const_month = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
t_f = True
stopped = list()


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


def on_off(ctx):
    global t_f, stopped, voice
    t_f = True
    os.remove('song.mp3')
    print('Закон.')
    stopped.remove(stopped[0])
    if len(stopped) != 0:
        t_f = False
        url = stopped[0]
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
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: on_off(ctx))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1


@ibio.command()
async def включи(ctx, url : str):
    global t_f, voice, stopped
    stopped.append(url)
    print(stopped)
    url = stopped[0]
    if len(stopped) >= 2:
        await ctx.message.channel.send(f'Сейчас играет:\n{stopped[0]}\nследующий:\n{stopped[1]}\n\n```Пропишите !следующий для пропуска музыки```')
    if t_f:
        try:
            t_f = False
            song_there = os.path.isfile('song.mp3')
            try:
                if song_there:
                    os.remove('song.mp3')
            except PermissionError:
                pass
            await ctx.message.channel.send('Подождите...')
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
                    os.rename(file, 'song.mp3')
            voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: on_off(ctx))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 1
        except Exception:
            pass


@ibio.command()
async def следующий(ctx):
    global voice
    voice.stop()


ibio.run(TOKEN)