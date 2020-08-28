import discord
from discord.ext import commands
import json

import asyncio

import cogs._json


class Member(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Member Cog has been loaded\n-----")

    # สำหรับลงทะเบียน
    @commands.command(name="register",
                      description="ลงทะเบียนสมาชิกเพื่อเข้าร่วมการแข่งขัน",
                      aliases=['reg', 'regist'],
                      )
    async def register(self, ctx):
        db = cogs._json.read_json("user_data")
        await ctx.send("กำลังลงทะเบียน...")

        # ลงทะเบียนพร้อมกับตรวจสอบ
        if await Member.update_data(self, db, ctx.author):
            await ctx.send(f"ลงทะเบียนเรียบร้อยแล้วค่ะ")
        else:
            await ctx.send(f"ท่านเคยลงทะเบียนไปแล้วนะคะ")

        cogs._json.write_json(db, "user_data")
        #print (db[str(ctx.author.id)]['level'])
        ''' กำลังศึกษาส่วนนี้
        try:
            pass
            nickn = f"[{db[str(ctx.author.id)]['level']}]{db[str(ctx.author.id)]['name']}"
            await ctx.author.edit(nick=nickn)
        except discord.DiscordException:
            
            pass
        finally:
            pass
        '''

    # เพิ่ม xp ตามจำนวน
    @commands.command(name="addexp",
                      description="เพิ่ม exp ให้กับ user (Bot_Owner only)",
                      aliases=['addxp'],
                      usage="<@ชื่อ หรือ id> <จำนวน xp>",
                      )
    @commands.is_owner()
    async def addexp(self, ctx, member: discord.Member = None, xp: int = None):

        if member is None or xp is None:
            await ctx.send("ต้องใส่ <@ชื่อ หรือ id> <จำนวน xp> ด้วยค่ะ")
            return

        db = cogs._json.read_json("user_data")

        await Member.update_data(self, db, member) # เป็นการเพิ่มสมาชิกให้ใหม่เลย ตรงนี้แก้ภายหลัง

        db[str(member.id)]["exp"] += xp

        cogs._json.write_json(db, "user_data")

        await ctx.send(f"ได้เพิ่ม {xp} exp ให้กับ {member} แล้วค่ะ")

    '''
    เป็นส่วนของการเข้าถึงการครวจสอบข้อมูล
    '''

    async def update_data(self, users, user):
        uid = str(user.id)
        if not uid in users:
            users[uid] = {}
            users[uid]["name"] = user.name
            users[uid]["point"] = 0
            users[uid]["xp"] = 0
            users[uid]["level"] = 1
            users[uid]["qtime"] = 0

            return True
        else:
            return False

    async def is_reg(self, users, user):
        uid = str(user.id)
        return uid in users


def setup(bot):
    bot.add_cog(Member(bot))
