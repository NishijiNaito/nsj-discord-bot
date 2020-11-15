import discord
from discord.ext import commands
import json
from datetime import datetime
from pythainlp.util import eng_to_thai
from pythainlp.tokenize import syllable_tokenize
import asyncio

import cogs._json


class Thaifunction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Thaifunction Cog has been loaded\n-----")

    # waitfor1
    @commands.command(name="de",
                      description="ลืมกดภาษาใช่มั๊ย เอาสิ่งนี้ไปเลย ช่วยได้นะ",
                      aliases=['ttt'],
                      usage="<หมายเลขไอดี>",
                      )
    async def de(self,ctx, mid = None):
        
        if mid == None:
            return
        msg = await ctx.channel.fetch_message(mid)

        await ctx.channel.send(f"> {msg.content}\n{eng_to_thai(msg.content)}")

    @commands.command(name="reverse",
                      description="ย้อนพยาางค์ สร้างความสับสน",
                      aliases=['rev'],
                      usage="<ประโยค>",
                      )
    async def reverse(self,ctx, *, sen = None):
        
        if sen == None:
            await ctx.channel.send(f"โปรดป้อนคำตอบด้วยค่ะ", delete_after=10)
            return
        
        rev = ''

        for wor in syllable_tokenize(sen)[::-1]:
            rev = rev + wor


        await ctx.channel.send(f"> {sen}\n{rev}")



def setup(bot):
    bot.add_cog(Thaifunction(bot))


'''
embed = discord.Embed(title="คำถามประจำวันที่ 26/08/2020", colour=discord.Colour(0x4a90e2), description="รายละเอียดคำถาม", timestamp=datetime.datetime.utcfromtimestamp(1598459592))

embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
embed.set_author(name="author name", icon_url="https://cdn.discordapp.com/embed/avatars/3.png")
embed.set_footer(text="Nishiji Quiz", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

embed.add_field(name="exp", value="```50```", inline=True)
embed.add_field(name="point reward", value="```50```", inline=True)
embed.add_field(name="คำถาม?", value="```ตัวพระเอกในอนิเมะเรื่อง Princess Connect Redive คือใคร?```")
embed.add_field(name="คุณมีโอกาสในการตอบคำถามนี้เพียงครั้งเดียวเท่านั้น", value="```\nสามารถส่งคำตอบได้โดยการพิมพ์คำสั้ง\nnq.ans <คำตอบ>```")

await bot.say(embed=embed)
'''
