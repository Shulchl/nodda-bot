import discord, asyncio
from discord.ext import commands  

# This prevents staff members from being punished 
class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        else:
            raise await ctx.send.commands.BadArgument("Você não pode punir um moderator") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Mutado") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        else:
            raise commands.BadArgument("O usuario não foi mutado.") # self-explainatory
            
# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx, user, reason):
    role = discord.utils.get(ctx.guild.roles, name="Mutado") # retrieves muted role returns none if there isn't 
    channel = discord.utils.get(ctx.guild.text_channels, name="inferno") # retrieves channel named inferno returns none if there isn't
    if not role: # checks if there is muted role
        try: # creates muted role 
            muted = await ctx.guild.create_role(name="Mutado", reason="Usado para mutar")
            for channel in ctx.guild.channels: # removes permission to view and send in the channels 
                await channel.set_permissions(muted, send_messages=False,
                                            read_message_history=False,
                                            read_messages=False)
        except discord.Forbidden:
            return await ctx.send("Eu não tenho permissão para criar um cargo mutado.") # self-explainatory
        await user.add_roles(muted) # adds newly created muted role
        await ctx.send("{} foi mandado ao {} por {}".format(user.mention, channel, reason))
    else:
        await user.add_roles(role) # adds already existing muted role
        await ctx.send("{} foi mandado ao {} por {}".format(user.mention, channel, reason))
        
    if not channel: # checks if there is a channel named inferno
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=True),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=False),
                        muted: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel
        try: # creates the channel and sends a message
            channel = await ctx.create_channel('inferno', overwrites=overwrites)
            await channel.send("Seja bem vindo ao {}.. Você foi exilado para cá até que seja desmutado. Aprecie o silêncio.".format(channel))
        except discord.Forbidden:
            return await channel.send("Eu não tenho permissão para criar o {}".format(channel))

class Moderation(commands.Cog, name='Moderação'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog de Moderação funcionando!    [√]')

    @commands.command(name='mute', help='Muta um usuário ao digitar `&mute <usuário>`')
    async def mute(self, ctx, user: Sinner, reason=None):
        #"""Gives them inferno."""
        await mute(ctx, user, reason or "Desrespeito às regras.") # uses the mute function
        channel = discord.utils.get(ctx.guild.text_channels, name="inferno")
        embed = discord.Embed(title=f"Olá, seja bem vindo ao {channel}.\n Você foi exilado para cá até que seja desmutado.",
                            description="Aprecie o silêncio", color=0)
        msg = await channel.send(embed=embed)
        await channel.send(user.mention)
        

    @commands.command(name='unmute', help='Desmuta um usuário ao digitar `%unmute <usuário>`')
    async def unmute(self, ctx, user: Redeemed):
        #"""Unmutes a muted user"""
        unmu = discord.utils.get(ctx.guild.roles, name="Mutado")
        await user.remove_roles(unmu) # removes muted role
        await ctx.send(f"{user.mention} foi desmutado.")
                
    @commands.command(name='clear', help='Limpa um determinado número de mensagens ao digitar `&clear <número>`')
    @commands.has_any_role("Moderador", "Moderator", "Helper")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount + 1)
        await asyncio.sleep(2)
        emb = discord.Embed(title='Limpei!',description='{} mensagens foram apagadas!'.format(amount),color=discord.Color.red())
        await ctx.send('',embed=emb)
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)  
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send('Você precisa colocar o número de mensagem que deseja apagar.')

    @commands.command(name='kick', help='Chuta um usuário para fora do servidor ao digitar `&kick <usuário>`')
    @commands.has_any_role("Moderador", "Moderator")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member : discord.Member, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} from the server.')

    @commands.command(name='ban', help='Bane um usuário do servidor ao digitar `&ban <usuário>`')
    @commands.has_any_role("Moderador", "Moderator")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(self, ctx, member : discord.Member, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} from the server.')

    @commands.command(name='unban', help='Revoga o banimento de um usuário do servidor ao digitar `&unban <usuário>`')
    @commands.has_any_role("Moderador", "Moderator")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} foi desbanido do servidor.')
                return

#    @commands.command(name='lock', help='locka `.lock`')
#    @commands.has_any_role("Moderador", "Moderator", "Helper")
#    @commands.cooldown(1, 10, commands.BucketType.user)
#    async def lock(self, ctx):
#            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)

#    @commands.command(name='unlock', help='unlocka `.unlock`')
#    @commands.has_any_role("Moderador", "Moderator", "Helper")
#    @commands.cooldown(1, 10, commands.BucketType.user)
#    async def unlock(self, ctx):
#            await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True,read_messages=True)

def setup(client):
    client.add_cog(Moderation(client))
