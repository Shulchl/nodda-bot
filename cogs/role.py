import discord
from discord.ext import commands
import discord.utils 
from discord.utils import get

class Role(commands.Cog, name='Cargos'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog de Cargos funcionando!       [√]')

    @commands.command(name='get', help='Recebe um determinado cargo ao digitar `%get <cargo>`')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        if not x:
            geth = discord.Embed(title='Erro!',description='There is not that role, my dear {}\n'.format(member.mention),color=discord.Color.red())
            await ctx.send('',embed=geth)
        elif x:
            await member.add_roles(role)
            geth = discord.Embed(title='Adicionado!',description='I have given the {}s role to the user {}'.format(role.name, member.mention),color=discord.Color.green())
            await ctx.send('',embed=geth)
        
    @commands.command(name='remove', help='Remove um cargo de sí mesmo ao digitar `%remove <cargo>`')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remove(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        if not x:
            geth = discord.Embed(title='Erro!',description='There is not that language role, my dear {}'.format(member.mention),color=discord.Color.red())
            await ctx.send('',embed=geth)
        elif x:
            await member.remove_roles(role)
            geth = discord.Embed(title='Removido!',description='I have removed the {}s role from the user {}'.format(role.name, member.mention),color=discord.Color.green())
            await ctx.send('',embed=geth)

def setup(client):
    client.add_cog(Role(client))