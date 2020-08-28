import discord
from discord.ext import commands
import json
from pathlib import Path
import logging
import datetime
import os
import asyncio
import re  # Regular Expression

import cogs._json
#ประกาศ current work directory
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


nak = ['นะค่ะ', 'เลยคะ', 'ไหมค่ะ', 'มั๊ยค่ะ', 'สวัสดีคะ', 'ขอบคุณคะ',
       'รักคะ', 'เกลียดคะ', 'เชิญคะ', 'จบคะ', 'ขอบใจคะ', 'ไปคะ', 'ไหวคะ', 'หัวคะ']

# สวัสดีค่ะ ขอบคุณค่ะ รักค่ะ เกลียดค่ะ เชิญค่ะ จบค่ะ
nonak = ['จะนะ', 'คาตาคานะค่ะ']

#bot = commands.Bot(command_prefix="nsm.")

'''
    คำเตือน
    ก่อนจะใช้งาน Bot ให้ไปที่ bot_config และไปใส่ Token พร้อมกับ prefix
'''
secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
#user_data = json.load(open(cwd+'/bot_config/user_data.json'))

'''
    คำเตือน
    ใน document จะใช้กันว่า client แต่ในที่นี้ขอใช้คำว่า bot นะ
    ถ้าเห็น bot ตรงไหน ตรงนั้นก็คือ client ใน Doc นั่นแหละ
'''

bot = commands.Bot(command_prefix=secret_file['prefix'],
                   case_insensitive=True,
                   owner_id=244841506148581376, #เปลี่ยนเป็นไอดีของตนเอง เพื่อเข้าถึงคำสั่งของ Owner
                   help_command=None
                   )

# เก็บค่าทุกสิ่งไว้ใน bot สามารถเปลี่ยนแปลงได้คลอดเวลา
bot.config_prefix = secret_file['prefix'] #เก็บข้อมูล Prefix ไว้ใน bot
bot.config_token = secret_file['token'] #เก็บข้อมูล Token
logging.basicConfig(level=logging.INFO)

#bot.blacklisted_users = [] #ตอนนี้ยังไม่ได้ใช้งาน

bot.cwd = cwd

bot.version = '2'

bot.colors = {
    'WHITE': 0xFFFFFF,
    'AQUA': 0x1ABC9C,
    'GREEN': 0x2ECC71,
    'BLUE': 0x3498DB,
    'PURPLE': 0x9B59B6,
    'LUMINOUS_VIVID_PINK': 0xE91E63,
    'GOLD': 0xF1C40F,
    'ORANGE': 0xE67E22,
    'RED': 0xE74C3C,
    'NAVY': 0x34495E,
    'DARK_AQUA': 0x11806A,
    'DARK_GREEN': 0x1F8B4C,
    'DARK_BLUE': 0x206694,
    'DARK_PURPLE': 0x71368A,
    'DARK_VIVID_PINK': 0xAD1457,
    'DARK_GOLD': 0xC27C0E,
    'DARK_ORANGE': 0xA84300,
    'DARK_RED': 0x992D22,
    'DARK_NAVY': 0x2C3E50
}
bot.color_list = [c for c in bot.colors.values()]


@bot.event
async def on_ready():
    '''
    game = discord.Game("ใช้ prefix nsm.")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    '''
    print(
        f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: {bot.config_prefix}\n-----")
    # This changes the bots 'activity'
    await bot.change_presence(activity=discord.Game(name=f"Hi, my names {bot.user.name}.\nใช้ {bot.config_prefix} เพื่อรันคำสั่ง"))

'''
    ส่วนนี้อาจจะเข้าไปใน cog ในรุ่นถัดไป
'''

@bot.event
async def on_message(message):  # ดักรอข้อความใน Chat 
    if message.author.id == bot.user.id:
        return

    if not any(re.findall('|'.join(nonak),  message.content.replace(' ', ''))):  # กรองคำเกือบไม่ถูก
        if any(re.findall('|'.join(nak), message.content.replace(' ', ''))):  # ลบ ถ้าเจอคำไม่ถูก
            # await message.delete()

            await message.channel.send('ใช้ คะ ค่ะ ให้ถูกนะคะ <@{0.author.id}> แต่ถ้าใช้ถูกแล้วก็ขอโทษด้วยค่าา T^T'.format(message), delete_after=10)

    await bot.process_commands(message)

'''
การจัดการเกี่ยวกับ Error ทั้งหลาย
ในตอนนี้ก็ยังไม่ชัดเจน
'''

@bot.event 
async def on_command_error(ctx, error):
    #print(f'error detected : {error}')
    # print(type(error))
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("ไม่มีคำสั่งนี้ค่ะ", delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()
    elif isinstance(error, commands.NotOwner):
        await ctx.send("คนที่สามารถใช้คำสั่งได้คือเจ้าของค่ะ", delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.send("ไม่มีส่วนเสริมนี้ค่ะ")


# load ext
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"ท่านได้โหลดส่วนเสริม {extension} นี้แล้วค่ะ")


@load.error
async def load_error(ctx, error):

    # print(error)

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("โปรดป้อนส่วนเสริมที่จะโหลดด้วยค่ะ")
    elif isinstance(error, commands.ExtensionError):
        await ctx.send(f"มีปัญหาค่ะ : {error}")
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send("ท่านได้โหลดส่วนเสริมนี้แล้วค่ะ")
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.send("ไม่มีส่วนเสริมนี้ค่ะ")

# unload extension
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"ท่านได้ปิดส่วนเสริม {extension} นี้แล้วค่ะ")


@unload.error
async def unload_error(ctx, error):

    # print(error)

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("โปรดป้อนส่วนเสริมที่จะโหลดด้วยค่ะ")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"ท่านได้รีโหลดส่วนเสริม {extension} นี้แล้วค่ะ")


# โหลดส่วนขยายตัวอื่นทั้งหมด ที่อยู่ใน Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith("_"):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(bot.config_token) #เริ่มการทำงาน
'''
    คำเตือน อีกครั้ง
    ใน document จะใช้กันว่า client แต่ในที่นี้ขอใช้คำว่า bot นะ
    ถ้าเห็น bot ตรงไหน ตรงนั้นก็คือ client ใน Doc นั่นแหละ
'''