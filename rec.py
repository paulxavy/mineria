import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient  # important!
#from secrets import token  # bot's secret token
import random
import json, os
import asyncio 

f = open('config.json')
config_data = json.load(f)
template = {'prefix': '!','token': ""}  
prefix = config_data["prefix"]
token = config_data["token"]

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print('im ready')


@client.command()
async def help(ctx):
    embedVar = discord.Embed(title="aquí estan mis comandos!",
                             description="user **!join** empezar a grabar\nuser **!stop** parar de grabar"
                             +"\nuser **!joinr** grabar automaticamente\nuser **!stop_auto** parar de grabar automaticamente", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect(cls=NativeVoiceClient)
    await ctx.invoke(client.get_command('rec'))


@client.command()
async def test(ctx):
    await ctx.send('hello im alive!')


@client.command()
async def rec(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = str(random.randint(000000, 999999))
    filepath = os.path.join('audios', f'{name}.flac') 
    with open(filepath, 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()


@rec.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect(cls=NativeVoiceClient)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

@client.command()
async def joinr(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect(cls=NativeVoiceClient)
    await ctx.invoke(client.get_command('rec_auto'))  # usamos la versión automática de la grabación


@client.command()
async def rec_auto(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Automatic Recording!",
                             description=f"Recording every 20 seconds. Use {prefix}stop_auto to stop.", color=0x546e7a)
    await ctx.send(embed=embedVar)
    await asyncio.sleep(20)  # esperamos 20 segundos antes de llamar a la función stop_auto
    await ctx.invoke(client.get_command('stop_auto'))


@client.command()
async def stop_auto(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Automatic Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = str(random.randint(000000, 999999))
    filepath = os.path.join('audios', f'{name}.flac')  # create the filepath
    with open(filepath, 'wb') as f:
        f.write(wav_bytes)
    
    
    await asyncio.sleep(20)  # esperamos otros 20 segundos antes de llamar a la función rec_auto
    await ctx.invoke(client.get_command('rec_auto'))
    
client.run(token)