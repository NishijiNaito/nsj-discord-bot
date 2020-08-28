import re
import math
import random

import discord
from discord.ext import commands

import cogs._json

'''
    ส่วนนี้ไปดูจากยูทูปมา ไว้ศึกษาทีหลัง 
    แต่ตรงนี้เป็นส่วนของคำสั่ง Help ไว้แสดงข้อมูลว่า ใช้ยังไง

'''
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name='help', aliases=['h'], description="The help command!"
    )
    async def help(self, ctx, cog="1"):
        helpEmbed = discord.Embed(
            title="Help commands!", color=random.choice(self.bot.color_list)
        )
        helpEmbed.set_thumbnail(url=ctx.author.avatar_url)

        # Get a list of all our current cogs & rmeove ones without commands
        cogs = [c for c in self.bot.cogs.keys()]
        #cogs.remove('Events')

        totalPages = math.ceil(len(cogs) / 4)

        if re.search(r"\d", str(cog)):
            cog = int(cog)
            if cog > totalPages or cog < 1:
                await ctx.send(f"ไม่พบหมายเลขหน้า: `{cog}`. โปรดใส่ตัวเลขหน้าที่มีค่าไม่เกิน {totalPages} \nหรือ แค่พิมพ์ `help` เพื่อดูรายการคำสั่ง")
                return

            helpEmbed.set_footer(
                text=f"<> - จำเป็น & [] - ตัวเลือก อาจจะไม่ใส่ก็ได้ | Page {cog} of {totalPages}"
            )

            neededCogs = []
            for i in range(4):
                x = i + (int(cog) - 1) * 4
                try:
                    neededCogs.append(cogs[x])
                except IndexError:
                    pass

            for cog in neededCogs:
                commandList = ""
                for command in self.bot.get_cog(cog).walk_commands():
                    if command.hidden:
                        continue

                    elif command.parent != None:
                        continue

                    commandList += f"**{command.name}** - *{command.description}*\n"
                commandList += "\n"

                helpEmbed.add_field(name=cog, value=commandList, inline=False)

        elif re.search(r"[a-zA-Z]", str(cog)):
            lowerCogs = [c.lower() for c in cogs]
            if cog.lower() not in lowerCogs:
                await ctx.send(f"ไม่พบชุดคำสั่ง: `{cog}`. โปรดใส่ตัวเลขหน้าที่มีค่าไม่เกิน {totalPages} \nหรือ แค่พิมพ์ `help` เพื่อดูรายการคำสั่ง หรือ พิมพ์ `help [ชุดคำสั่ง]` เพื่อดูวิธีการใช้คำสั่งในชุดคำสั่งนั้นๆ")
                return

            helpEmbed.set_footer(
                text=f"<> - จำเป็น & [] - ตัวเลือก อาจจะไม่ใส่ก็ได้ | ชุดคำสั่งที่ {(lowerCogs.index(cog.lower())+1)} จาก {len(lowerCogs)}"
            )

            helpText = ""

            for command in self.bot.get_cog(cogs[lowerCogs.index(cog.lower())]).walk_commands():
                if command.hidden:
                    continue

                elif command.parent != None:
                    continue

                helpText += f"```{command.name}```\n**{command.description}**\n\n"

                if len(command.aliases) > 0:
                    helpText += f'**Aliases: ** `{", ".join(command.aliases)}`'
                helpText += '\n'
                '''
                data = await self.bot.config._Document__get_raw(ctx.guild.id)
                if not data or "prefix" not in data:
                    prefix = self.bot.DEFAULTPREFIX
                else:
                    prefix = data['prefix']
                '''
                #data = cogs._json.read_json('secrets')
                #prefix = data['prefix']
                
                #prefix = "nsj."

                prefix = self.bot.config_prefix
                helpText += f'**Format:** `{prefix}{command.name} {command.usage if command.usage is not None else ""}`\n\n'
            helpEmbed.description = helpText

        else:
            await ctx.send(f"ไม่พบชุดคำสั่ง: `{cog}`\nโปรดใส่ตัวเลขหน้าที่มีค่าไม่เกิน {totalPages} \nหรือ แค่พิมพ์ `help` เพื่อดูรายการคำสั่ง หรือ พิมพ์ `help [ชุดคำสั่ง]` เพื่อดูวิธีการใช้คำสั่งในชุดคำสั่งนั้นๆ")
            return

        await ctx.send(embed=helpEmbed)


def setup(bot):
    bot.add_cog(Help(bot))
