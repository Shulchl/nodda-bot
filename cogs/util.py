import discord
from discord.ext import commands
import discord.utils 
from discord.utils import get

class Util(commands.Cog, name='Utilidades'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog de Comandos Úteis funcionando!       [√]')

    @commands.command(name='ajudar', help='Comando usado para avisar desavisados digitando `&ajudar <usuário>`.')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ajudar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        regras = discord.utils.get(ctx.guild.text_channels, name="regras")
        outros = discord.utils.get(ctx.guild.text_channels, name="outros")
        geth = discord.Embed(title='Antes de qualquer coisa, leia as {}, {}!'.format(regras, member),description='Não pergunte se alguém pode te ajudar. Se você leu as #{}, você sabe o que fazer!'.format(regras),color=discord.Color.green())
        await ctx.send('',embed=geth)

    @commands.command(name='canal', help='Comando usado para avisar desavisados digitando `&canal <usuário>`.')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def canal(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        regras = discord.utils.get(ctx.guild.text_channels, name="regras")
        outros = discord.utils.get(ctx.guild.text_channels, name="outros")
        geth = discord.Embed(title='Antes de qualquer coisa, leia as {}, {}!'.format(regras, member),description='Tem algum erro no seu código ou precisa de ajuda com alguma lingua, mande a sua dúvida, a situação que gerou essa dúvida e o código no canal específico da linguagem.\n\nNão achou o canal? Mande em #{}! \n\nCom certeza alguém irá te ajudar!'.format(outros),color=discord.Color.green())
        await ctx.send('',embed=geth)
        
    @commands.command(name='projeto', help='Comando usado para avisar desavisados digitando `&projeto <usuário>`.')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def projeto(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        regras = discord.utils.get(ctx.guild.text_channels, name="regras")
        projetos = discord.utils.get(ctx.guild.text_channels, name="projetos")
        geth = discord.Embed(title='Antes de qualquer coisa, leia as {}, {}!'.format(regras, member),description='É um projeto não renumerado? Então mande em #{}, mas leia a descrição do canal antes! \n\nBoa sorte!'.format(projetos),color=discord.Color.green())
        await ctx.send('',embed=geth)
    
    @commands.command(name='emprego', help='Comando usado para avisar desavisados digitando `&emprego <usuário>`.')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emprego(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        regras = discord.utils.get(ctx.guild.text_channels, name="regras")
        trabalho = discord.utils.get(ctx.guild.text_channels, name="ofertas-de-trabalho")
        geth = discord.Embed(title='Antes de qualquer coisa, leia as {}, {}!'.format(regras, member),description='É um projeto renumerado? Uma oferta de emprego? Então mande em #{}, mas leia a descrição do canal antes! \n\n **Projetos valendo ações não contam como renumerados.** \n\nBoa sorte!'.format(trabalho),color=discord.Color.green())
        await ctx.send('',embed=geth)

def setup(client):
    client.add_cog(Util(client))
