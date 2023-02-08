# This example requires the 'message_content' intent.
import discord
from tabulate import tabulate
from descargar_data import traer_data,fecha,symbols
from api import api

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#lista


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message.content.startswith('$')
    ticker = (message.content[1:]).upper()   
    if not ticker in symbols :
         await message.channel.send(f' Ticker no valido {message.author} ')
    else:
        fecha_valida = fecha(12)
        data = traer_data(ticker,fecha_valida,fecha_valida)
        especie = data['especie'][0]
        fecha_ = data['fecha'][0]
        apertura = int(data['apertura'])
        cierre = int(data['cierre'])
        volumen = int(data['volumen'])
        mensaje = "```" + tabulate([[especie,apertura,cierre,volumen,fecha_]],
                    headers = ['Especie','Apertura', 'Cierre', 'Volumen','Fecha'],
                    tablefmt = 'fancy_grid',
                    stralign='left',
                    numalign='left',
                    floatfmt=".2f")+"```"
        await message.channel.send(mensaje)
           

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Tirando notas'))


client.run(api)

