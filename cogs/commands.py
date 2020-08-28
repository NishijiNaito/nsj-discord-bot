import discord
from discord.ext import commands
import platform

import cogs._json


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Commands Cog has been loaded\n-----")

    @commands.command(
        name="stats",
        description="ตรวจสอบสถานะของบอท",

    )
    async def stats(self, ctx):
        """
        A usefull command that displays bot statistics.
        """
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF',
                              colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developers:', value="NiShiJi_NaiTo")

        embed.set_footer(text=f"Carpe Noctem | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    # หยุดการทำงาน
    @commands.command(aliases=['disconnect', 'close', 'stopbot'],
                      name="logout",
                      description="หยุดการทำงานของบอท",

                      )
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from discord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    
    @commands.command(
        name="echo",
        description="ให้ bot ประกาศข้อความตามที่เขียน",
        usage="<ข้อความ>",
    )
    async def echo(self, ctx, *, message=None):
        """
        A simple command that repeats the users input back to them.
        """
        message = message or "โปรดป้อนข้อความที่จะประกาศด้วยค่ะ"
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(pass_context=True,
                      name="chnick",
                      description="เปลี่ยนชื่อเล่นของคนๆ นั้น (Bot_Owner only)",
                      usage="<@ชื่อ> <ชื่อที่จะเปลี่ยน>",
                      )
    @commands.is_owner()
    async def chnick(self, ctx, member: discord.Member, *, nickname: str):
        await member.edit(nick=nickname)
        await ctx.send(f'Nickname was changed for {member.mention} ')

    @commands.command(pass_context=True,
                      name="send",
                      description="ให้ bot ส่งข้อความไปยังห้องที่กำหนด",
                      usage="<#ห้องแชท> <ข้อความ>",
                      )
    #@commands.is_owner()
    async def send(self, ctx, txtcha: discord.TextChannel = None, *, text: str = None):
        if not txtcha is None:
            if not text is None:
                await ctx.message.delete()
                await txtcha.send(f'{text}')
            else:
                await ctx.send(f'กรอกข้อความที่ต้องการจะส่งด้วยค่ะ')
        else:
            await ctx.send(f'กรุณาเลือกช่องข้อความที่จะส่งด้วยค่ะ')

    @commands.command(pass_context=True,
                      name="chmynick",
                      description="เปลี่ยนชื่อเล่นของตนเอง",
                      usage="<ชื่อเล่นที่จะเปลี่ยน>",
                      )
    async def chmynick(self, ctx, *, nickname: str = None):
        if not nickname is None:
            await ctx.author.edit(nick=nickname)
            await ctx.send(f'ชื่อของท่านได้เปลี่ยนแล้วค่ะ')
        else:
            await ctx.send(f'กรอกชื่อที่ต้องการเปลี่ยนด้วยค่ะ')


def setup(bot):
    bot.add_cog(Commands(bot))
