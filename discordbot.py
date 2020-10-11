import discord, os, asyncio, random
from discord.ext import commands
from datetime import date, datetime, timedelta  

date = date.today()

client = commands.Bot(command_prefix = "&")

client.remove_command('help')


@client.event
async def on_ready():
    print('To logada como {0.user}'.format(client))
    try:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the errors' log"))
        print(f'Tudo perfeito!'.format(client))
    except:
        print(f'Não foi possivel adicionar uma atividade.'.format(client))

        
        
#@client.event
#async def hidratar():
#    await client.wait_until_ready()
#    channel = client.get_channel(686235454458298441)
#    while not client.is_closed():
#        try:
#            await channel.send(f'**Se hidratem!**')
#            await asyncio.sleep(random.choice([1100, 1300, 1350, 1500, 1800]) + 1800)
#        except:
#            print(f'Não consegui mandar hidratar')
#            await asyncio.sleep(1800)
            
@client.event
async def count():
    await client.wait_until_ready()
    guild = client.get_guild(685932057657868289)
    channel = client.get_channel(763193483312889906)
    while not client.is_closed():
        try:
            total = guild.member_count
            await channel.edit(name=f'{total}𝐦𝐞𝐦𝐛𝐫𝐨𝐬')
            await asyncio.sleep(3)
        except:
            print('Não consegui pegar o total de membros')
            await asyncio.sleep(3)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{error}')

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"I have loaded the command")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("I have reloaded the command")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("I have unloaded the command")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(count())
client.loop.create_task(hidratar())
client.run(os.getenv('TOKEN'))
