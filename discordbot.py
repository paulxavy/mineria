import json, os
from discord.ext import commands
import discord
from discord.ext.commands import has_permissions
import pydub
import pydub.audio_segment
import io
import os

MAX_RECORDING_LENGTH = 20  # segundos
def main():
    if  os.path.exists('config.json'):
        with open('config.json') as f:
            config_data = json.load(f)
    else:
        template = {'prefix': '!','token': ""}
        with open('config.json','w') as f:
            json.dump(template,f)
        print('Creando archivo de configuración')
    prefix = config_data["prefix"]
    token = config_data["token"]
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = prefix, intents = intents, description = 'Bot moderador')
    
    @bot.command(name='saludar', help='El bot te saludara')
    async def saludar(ctx):
     await ctx.reply(f'Hola {ctx.author}, Como estas?')   
    @bot.command(name='grabar', help='El bot grabara')
    async def grabar(ctx):
        # Esperar hasta que se conecte un usuario
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()

        # Crear un segmento de audio en blanco para agregar los clips grabados
        audio_segment = pydub.AudioSegment.silent(duration=0)

        # Grabar audio en clips hasta que el tiempo máximo de grabación sea alcanzado o se envíe el comando !stop
        while audio_segment.duration_seconds <= MAX_RECORDING_LENGTH :
            # Recibir paquetes de audio del servidor por un corto período de tiempo
            audio_source = voice_client.record()
            audio_data = await audio_source

            # Crear un segmento de audio a partir de los datos de audio y agregarlo al segmento general
            audio_clip = pydub.AudioSegment(data=audio_data, sample_width=2, frame_rate=48000, channels=2)
            audio_segment += audio_clip

        # Desconectar del canal de voz
        await voice_client.disconnect()

        # Guardar el audio en un archivo FLAC en la carpeta "voice"
        if not os.path.exists("voice"):
            os.mkdir("voice")
        output_file = os.path.join("voice", f"{ctx.message.created_at.strftime('%Y-%m-%d %H-%M-%S')}.flac")
        audio_segment.export(output_file, format="flac")
        await ctx.send(file=discord.File(output_file))
        os.remove(output_file)  # Eliminar archivo de audio temporal
    @bot.command(name='stop', help='El bot parara de grabar')
    async def stop(ctx):
        # Detener la grabación y desconectar del canal de voz
       
        await ctx.voice_client.disconnect()
    bot.run(token)



if __name__ == '__main__':
	main()