import asyncio
import discord
import re  # Regular Expression
import os

from discord.ext import commands, tasks

curse = ["ควย", "หี", 'เหี้ย', 'สัส', 'กะหรี่',
         'fuck', 'shit', 'shutup', 'อีดอก', 'เย็ด', 'ดอ']

uncurse = ["หีบ", 'กะหรี่ปั๊บ', 'แกงกะหรี่', 'ดอก', 'ดอง', 'ดอม']
#หมวดกรองคำหยาบ
class Curseword(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events Cog has been loaded\n-----")


    @commands.Cog.listener()
    async def on_message(self,message):
        if not any(re.findall('|'.join(uncurse),  message.content.replace(' ', ''))):  # กรองคำเกือบหยาบ
            if any(re.findall('|'.join(curse), message.content.replace(' ', ''))):  # ลบ ถ้าเจอคำหยาบ
                await message.delete()
                await message.channel.send('พูดคำหยาบไม่ดีนะคะ <@{0.author.id}>'.format(message), delete_after=5)
        #await self.bot.process_commands(message)
    
    # commands
    @commands.command()
    async def cw(self, ctx):
        await ctx.send(f'เป็นระบบไว้ลบคำหยาบค่ะ <@{ctx.author.id}>')


def setup(bot):
    bot.add_cog(Curseword(bot))
