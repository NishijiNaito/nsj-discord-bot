import discord
from discord.ext import commands
import json

import asyncio

import cogs._json

'''
ส่วนนี้ไว้ทดสอบว่าแต่ละอย่าง ทำงานยังไง ตอนโหลดไป ลบอันนี้ไปเลยก็ได้นะ
'''

class Btest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Btest Cog has been loaded\n-----")

    # waitfor1
    @commands.command(name="wf1",
                      description="ทดสอบสำหรับ waitfor",

                      )
    async def wf1(self, ctx):
        # เก็บข้อมูลนี้เพื่อเช็คว่าเหตุการณ์อยู่ใน channel ที่พิมพ์คำสั่งไหม
        channel = ctx.channel
        # ให้รู้ว่าสามารถเก็บข้อความมาอ้างอิงได้นะ
        msgb = await channel.send('Say hello!')

        def check(m):  # จะประกาศสิ่งนี้เพื่อใช้ตรวจสอบ อาจจะไม่ใช่คำว่า check ก็ได้ แต่ต้องรับตัวแปร message เพื่อเอาไปตรวจสอบข้อความที่พิมพ์
            # บรรทัดนี้ ตรวจสอบว่า เป็นคำว่า hello ใน channel ที่พิมพ์คำสั่งไหม
            return m.content == 'hello' and m.channel == channel

        try:
            # เรียกให้รอข้อความจากคนที่พิมพ์ข้อความ โดยรอ 10 วิ
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:  # หมดเวลาในการโต้ตอบ ไม่ผ่านเงื่อนไข

            await msgb.delete()
            await channel.send('Bye  {.author.mention}!'.format(ctx))
            return  # ออกจากการทำงาน
        else:  # ผ่านเงื่อนไขจาก check
            await msg.delete()
            await msgb.delete()
            await channel.send('Hello  {.author.mention}!'.format(ctx))
        await channel.send('Finish  {.author.mention}!'.format(ctx))

    # waitfor many
    @commands.command(name="wfm",
                      description="ทดสอบสำหรับ waitfor many",

                      usage="<จำนวนรอบ>",
                      )
    @commands.is_owner()
    async def wfm(self, ctx, amount: int = None):
        pass

    # waitfor emoji
    @commands.command(name="wfe",
                      description="ทดสอบสำหรับ waitfor emoji",

                      )
    @commands.is_owner()
    async def wfe(self, ctx, amount: int = None):
        chan = ctx.channel
        msg = await chan.send('Send me that 👍 reaction, mate')
        await msg.add_reaction("👍")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.delete()
            await chan.send('👎')
        else:
            await msg.delete()
            await chan.send('👍')


def setup(bot):
    bot.add_cog(Btest(bot))


'''
embed = discord.Embed(title="คำถามประจำวันที่ 26/08/2020", colour=discord.Colour(0x4a90e2), description="รายละเอียดคำถาม", timestamp=datetime.datetime.utcfromtimestamp(1598459592))

embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
embed.set_author(name="author name", icon_url="https://cdn.discordapp.com/embed/avatars/3.png")
embed.set_footer(text="Nishiji Quiz", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

embed.add_field(name="exp", value="```50```", inline=True)
embed.add_field(name="point reward", value="```50```", inline=True)
embed.add_field(name="คำถาม?", value="```พระเอกในอนิเมะเรื่อง Princess Connect Redive คือใคร?```")
embed.add_field(name="คุณมีโอกาสในการตอบคำถามนี้เพียงครั้งเดียวเท่านั้น", value="```\nสามารถส่งคำตอบได้โดยการพิมพ์คำสั้ง\nnq.ans <คำตอบ>```")

await bot.say(embed=embed)
'''
