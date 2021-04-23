import discord
from discord.ext import commands
import datetime
from discord.utils import get
import youtube_dl
import os

commander = '*'
TOKEN = ""
ibio = commands.Bot(command_prefix=commander)
const_month = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
               'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
t_f = False
stopped = list()


@ibio.event
async def on():
    print('Запуск')


@ibio.command()
async def ready(ctx):
    global t_f
    await ctx.message.channel.send('```IBIO``` подключён.')
    await ctx.message.author.voice.channel.connect(reconnect=False)
    t_f = True


@ibio.command()
async def IBIO_help(ctx):
    await ctx.message.channel.send('```IBIO комманды:\n'
                                   'ready - вкл/выкл бот\n'
                                   'clarify "исчесление времени" - говорит время\n'
                                   'play "ссылка на видео с ютуба" - проигрывает музыку\n'
                                   'rem "Любые символы" - запоминает вашу фразу\n'
                                   'tell - воспроизводит ваши воспоминания\n'
                                   '\n'
                                   '\n'
                                   f'ВСЕ КОММАНДЫ ВВОДИТЬ С "{commander}".```')


@ibio.command()
async def clarify(ctx, args):
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
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
    except PermissionError:
        pass
    print('Закон.')
    stopped.remove(stopped[0])
    if len(stopped) != 0:
        try:
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
        except Exception:
            on_off(ctx)


@ibio.command()
async def play(ctx, url : str):
    global t_f, voice, stopped
    stopped.append(url)
    print(stopped)
    url = stopped[0]
    if len(stopped) >= 2:
        await ctx.message.channel.send(f'Сейчас играет:\n{stopped[0]}\nследующий:\n{stopped[1]}\n\n```Пропишите *skip для пропуска музыки```')
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
            on_off(ctx)


@ibio.command()
async def skip(ctx):
    global voice
    voice.stop()


@ibio.command()
async def rem(ctx, *arg):
    author = ctx.message.author
    information = '#- ' + ' '.join(arg) + ' -#'
    if '~~~' not in information and '===' not in information and '+++' not in information:
        file1 = open('remember_user/all_member_user.txt', mode='rt')
        old_inf = (file1.read()).split('~~~')
        print(old_inf)
        file = open('remember_user/all_member_user.txt', mode='w')
        print(str('~~~'.join(old_inf)))
        if str(author.mention) in str('~~~'.join(old_inf)):
            for i in range(1, len(old_inf)):
                if (old_inf[i].split('+++'))[0] == str(author.mention):
                    information = str((old_inf[i].split('+++'))[1]) + '===' + information
                    old_inf[i] = str(author.mention) + '+++' + information
                    break
            itog = '~~~'.join(old_inf)
            file.write(f'{itog}')
            file.close()
        else:
            old_inf = '~~~'.join(old_inf)
            file.write(f'{old_inf}~~~{author.mention}+++{information}')
            file.close()
        await ctx.message.channel.send(f'{author.mention}, Ваше напоминание запомнено...')
    else:
        await ctx.message.channel.send(f'{author.mention}, ваше напоминание содержит недопустимые символы: ~~~')


@ibio.command()
async def tell(ctx):
    author = ctx.message.author
    file1 = open('remember_user/all_member_user.txt', mode='rt')
    old_inf = (file1.read()).split('~~~')
    print(str('~~~'.join(old_inf)))
    if str(author.mention) in str('~~~'.join(old_inf)):
        for i in range(1, len(old_inf)):
            if (old_inf[i].split('+++'))[0] == str(author.mention):
                sss = '\n'.join(((old_inf[i].split('+++'))[1]).split('==='))
                await ctx.message.channel.send(f'Напоминания {author.mention} :\n'
                                               f'```{sss}```')
                break
    else:
        await ctx.message.channel.send(f'{author.mention}, Вы ещё не делали напоминаний')



ibio.run(TOKEN)