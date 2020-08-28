import discord
from discord.ext import commands
import json
from datetime import datetime
import asyncio

import cogs._json


class Quiz(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quiz Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.channel.id == 748537605389549629:  # ถ้าอยู่ห้องนี้ ไม่ต้องลบ
            return
        if message.author.id == self.bot.user.id:  # บอทที่รันขียน ไม่ต้องลบ
            return
        # ถ้าขึ้นต้นด้วยอันนี้ ไม่ต้องลบ
        if message.content.startswith(f'{self.bot.config_prefix}ans'):
            return
        # ถ้าขึ้นต้นด้วยอันนี้ ไม่ต้องลบ
        if message.content.startswith(f'{self.bot.config_prefix}qstart'):
            return
        # ถ้าขึ้นต้นด้วยอันนี้ ไม่ต้องลบ
        if message.content.startswith(f'{self.bot.config_prefix}qs'):
            return
        # ถ้าขึ้นต้นด้วยอันนี้ ไม่ต้องลบ
        if message.content.startswith(f'{self.bot.config_prefix}quizstart'):
            return

        #กรณีอื่น ลบมันนน
        try:
            if not message.content.startswith(f'{self.bot.config_prefix}'):

                await message.delete()
            else:
                await asyncio.sleep(6)
                await message.delete()
        except:
            pass

    # makequiz

    @commands.command(name="makequiz",
                      description="สร้างคำถาม",
                      aliases=['mq', 'mkq', 'mkquiz']
                      )
    @commands.is_owner()
    async def makequiz(self, ctx):
        #สร้างเพื่อเก็บข้อมูลคำถาม
        mquiz = {}
        # เก็บข้อมูลนี้เพื่อเช็คว่าเหตุการณ์อยู่ใน channel ที่พิมพ์คำสั่งไหม
        channel = ctx.channel

        # สร้างการตรวจสอบ ว่าคนเขียนเป็นคนพิมพ์คำสั่ง
        def check(m):
            return m.author == ctx.author and m.channel == channel
        # 1. ตั้งคำถาม question
        msgb = await channel.send('เริ่มต้นจากสิ่งแรก โปรดกรอกคำถามที่คุณจะตั้งภายใน 120 วินาที\nหรือ โปรดพิมพ์ end ถ้าจะยกเลิกการสร้างคำถาม')

        try:
            # เรียกให้รอข้อความจากคนที่พิมพ์ข้อความ โดยรอ 120 วิ
            msg = await self.bot.wait_for('message', timeout=120.0, check=check)
        except asyncio.TimeoutError:  # หมดเวลาในการโต้ตอบ ไม่ผ่านเงื่อนไข

            await msgb.delete()
            await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
            return  # ออกจากการทำงาน
        else:  # ผ่านเงื่อนไขจาก check 
            if msg.content == 'end': #ตรวจสอบว่า พิมพ์แค่คำว่า end หรือไม่
                await msg.delete()
                await msgb.delete()
                await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                return

        mquiz['question'] = msg.content
        await msg.delete()
        
        # 2. ตั้งคำตอบ
        await msgb.edit(content=f"สิ่งที่สอง โปรดป้อนคำตอบที่ถูกต้องของคำถามนี้\n```{mquiz['question']}```\nโดยถ้ามีหลายคำตอบ โปรดคั่นด้วย | ภายใน 120 วินาที\nหรือ โปรดพิมพ์ end ถ้าจะยกเลิกการสร้างคำถาม")
        try:
            # เรียกให้รอข้อความจากคนที่พิมพ์ข้อความ โดยรอ 120 วิ
            msg = await self.bot.wait_for('message', timeout=120.0, check=check)
        except asyncio.TimeoutError:  # หมดเวลาในการโต้ตอบ ไม่ผ่านเงื่อนไข

            await msgb.delete()
            await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
            return  # ออกจากการทำงาน
        else:  # ผ่านเงื่อนไขจาก check
            if msg.content == 'end':
                await msg.delete()
                await msgb.delete()
                await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                return

        mquiz['answer'] = msg.content.split('|')
        await msg.delete()

        # 3. ตั้งค่า xp
        while True:
            await msgb.edit(content="สิ่งที่สาม โปรดป้อนค่า xp ของคำถามนี้ในกรณีที่ตอบถูก ภายใน 30 วินาที\nหรือ โปรดพิมพ์ end ถ้าจะยกเลิกการสร้างคำถาม")
            try:
                # เรียกให้รอข้อความจากคนที่พิมพ์ข้อความ โดยรอ 30 วิ
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:  # หมดเวลาในการโต้ตอบ ไม่ผ่านเงื่อนไข

                await msgb.delete()
                await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                return  # ออกจากการทำงาน
            else:  # ผ่านเงื่อนไขจาก check
                if msg.content == 'end':
                    await msg.delete()
                    await msgb.delete()
                    await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                    return
            try:
                mquiz['xp'] = int(msg.content)
            except:
                await msg.delete()
                continue
            else:
                await msg.delete()
                break

        # 4. ตั้งค่า point
        while True:
            await msgb.edit(content="สิ่งสุดท้าย โปรดป้อนค่า point ของคำถามนี้ในกรณีที่ตอบถูก ภายใน 30 วินาที\nหรือ โปรดพิมพ์ end ถ้าจะยกเลิกการสร้างคำถาม")
            try:
                # เรียกให้รอข้อความจากคนที่พิมพ์ข้อความ โดยรอ 60 วิ
                msg = await self.bot.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:  # หมดเวลาในการโต้ตอบ ไม่ผ่านเงื่อนไข

                await msgb.delete()
                await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                return  # ออกจากการทำงาน
            else:  # ผ่านเงื่อนไขจาก check
                if msg.content == 'end':
                    await msg.delete()
                    await msgb.delete()
                    await channel.send('ยกเลิกการสร้างคำถาม', delete_after=10)
                    return

            try:
                mquiz['point'] = int(msg.content)
            except:
                await msg.delete()
                continue
            else:
                await msg.delete()
                break

        await msgb.delete()

        qc = cogs._json.read_json("quiz_config") #โหลดข้อมูลจาก quiz_config
        ql = cogs._json.read_json("quiz_list") #โหลดข้อมูลมาจาก quiz_list

        ql[str(qc["qgen"])] = mquiz #เอาข้อมูลที่เก็บมาไปใส่ใน ql

        cogs._json.write_json(ql, "quiz_list") #เอาข้อมูลใน ql ใส่คืนกลับไปในไฟล์

        embed = discord.Embed(title="คำถามที่ได้เพิ่มลงในฐานข้อมูลเรียบร้อยแล้ว",
                              colour=discord.Colour(0x4a90e2), description="รายละเอียดคำถาม")

        embed.set_thumbnail(url=str(self.bot.user.avatar_url))
        embed.set_author(name=str(self.bot.user.name),
                         icon_url=str(self.bot.user.avatar_url))
        embed.set_footer(text=f"{self.bot.user.name} Quiz",
                         icon_url=str(self.bot.user.avatar_url))

        embed.add_field(
            name="quiz_id", value=f"```{str(qc['qgen'])}```", inline=False)
        embed.add_field(name="exp", value=f"```{mquiz['xp']}```", inline=True)
        embed.add_field(
            name="point", value=f"```{mquiz['point']}```", inline=True)
        embed.add_field(
            name="คำถาม?", value=f"```{mquiz['question']}```", inline=False)
        embed.add_field(name="คำตอบ", value=f"```{mquiz['answer']}```")

        await channel.send(embed=embed) #ส่งข้อความ

        qc["qgen"] += 1 #เพิ่ม id ไปอีก 1 
        cogs._json.write_json(qc, "quiz_config") #เก็บค่า qc กลับเข้าไฟล์ quiz_config

    @commands.command(name="quizlist",
                      description="แสดงรายการคำถาม",
                      aliases=['ql']
                      )
    @commands.is_owner()
    async def quizlist(self, ctx):
        text = "" #เตรียมไฟล์ไว้เก็บข้อมูลเพื่อเอาไปใส่
        ql = cogs._json.read_json("quiz_list") #โหลดข้อมูล 
        if len(ql) == 0: #ถ้าในไฟล์ไม่มีคำถามใดๆ
            await ctx.channel.send(f"ไม่พบคำถาม")
            return
        #จะได้ข้อมูล ['quiz_id1(key)','quiz_id2(key)',...]
        '''
            คำอธิบาย ตัวอย่างข้อมูลใน quiz_list

            {
                "quiz_id1": {
                    "question": "5*4 = ?",
                    "answer": [
                        "20"
                    ],
                    "xp": 30,
                    "point": 50
                },
                "quiz_id2": {
                    "question": "5*3 = ?",
                    "answer": [
                        "15"
                    ],
                    "xp": 30,
                    "point": 50
                }
                
            }
            for q in ql: 
                จะได้ q แต่ละรอบเป็น "quiz_id1" และ "quiz_id2" ตามลำดับการเข้ามาของข้อมูล
                
                ผลลัพธ์ 1 กรณีที่ q เป็น quiz_id1
                ```
                quiz_id : quiz_id1 \n
                คำถาม : {ql['quiz_id1']['question']}\n
                คำตอบ : {ql['quiz_id1']['answer']}\n
                xp : {ql['quiz_id1']['xp']}\n
                point : {ql['quiz_id1']['point']}
                ```

        '''
        for q in ql: 
            #ดูคำอธิบายที่ ผลลัพธ์ 1
            text += f"```quiz_id : {q}\nคำถาม : {ql[str(q)]['question']}\nคำตอบ : {ql[str(q)]['answer']}\nxp : {ql[str(q)]['xp']}\npoint : {ql[str(q)]['point']}```\n"
            

        await ctx.channel.send(f"{text}")

    @commands.command(name="quizdelete",
                      description="ลบคำถามตาม id",
                      aliases=['qdel', 'quizdel'],
                      usage="<quiz_id>",
                      )
    @commands.is_owner()
    async def quizdelete(self, ctx, qid=None):
        ql = cogs._json.read_json("quiz_list")
        if qid == None:
            await ctx.message.delete()
            await ctx.channel.send(f"โปรดกรอก id ของคำถามที่จะลบด้วยค่ะ", delete_after=10)
            return

        try:
            del ql[str(qid)]
        except: #จากใน try ถ้ามันหาไม่เจอ จะเกิด Error เราเลยรู้ จึงไม่ได้ใส่ ว่าเป็น Error ประเภทไหน -0-
            await ctx.message.delete()
            await ctx.channel.send(f"ไม่พบ id {qid} ของคำถามที่จะลบค่ะ", delete_after=10)
            return

        cogs._json.write_json(ql, "quiz_list")#ถ้าลบเสร็จ ก็มาบันทึกที่นี่

        await ctx.channel.send(f"ลบคำถาม id {qid} เรียบร้อยแล้วค่ะ", delete_after=10)
        '''
        print(ql[str(qid)]) เคยลอง อย่าหาทำในตอนนี้
        if ql[str(qid)] == {}:
            await ctx.channel.send(f"ไม่พบ id {qid} ของคำถามที่จะลบค่ะ")
            pass
        '''

    @commands.command(name="quizstart",
                      description="เริ่มต้นคำถาม",
                      aliases=['qs', 'qstart'],
                      usage="<quiz_id>",
                      )
    @commands.is_owner()
    async def quizstart(self, ctx, qid=None):
        if qid == None:
            await ctx.message.delete()
            await ctx.channel.send(f"โปรดกรอก id ของคำถามที่จะเริ่มด้วยค่ะ", delete_after=10)
            return
        #โหลดข้อมูล 
        ql = cogs._json.read_json("quiz_list")
        qc = cogs._json.read_json("quiz_config")

        try: #เริ่มกระบวนการจับเออเร่อ
            quiz = ql[str(qid)] #จุดนี้ Error ได้ เพราะหาไม่เจอ
            qc['qtime'] += 1
            qc['now'] = qid
            embed = discord.Embed(title=f"คำถามครั้งที่ {qc['qtime']}",
                                  colour=discord.Colour(0x4a90e2), description=f"โปรดใช้คำสั่ง {self.bot.config_prefix}ans คำตอบที่ต้องการตอบ เพื่อตอบคำถามนี้")
            embed.set_thumbnail(url=str(self.bot.user.avatar_url))
            embed.set_author(name=str(self.bot.user.name),
                             icon_url=str(self.bot.user.avatar_url))
            embed.set_footer(text=f"{self.bot.user.name} Quiz",
                             icon_url=str(self.bot.user.avatar_url))

            embed.add_field(
                name="exp", value=f"```{quiz['xp']}```", inline=True)
            embed.add_field(
                name="point", value=f"```{quiz['point']}```", inline=True)
            embed.add_field(
                name="คำถาม?", value=f"```{quiz['question']}```", inline=False)

            #ถ้ารันมาถึงจุดนี้ได้ แสดงว่า idที่ค้นหา สามารถนำไปอ้างอิงได้ 
            cogs._json.write_json(qc, "quiz_config")
            await ctx.message.delete()
            await ctx.channel.send(embed=embed)
            # print(ql)
        except: # Error เพราะ id ไม่มีในข้อมูล
            await ctx.message.delete()
            await ctx.channel.send(f"ไม่พบ id {qid} ของคำถามที่จะลบค่ะ", delete_after=10)
            return


    # คำสั่งการตอบคำถาม
    @commands.command(name="answer",
                      description="ตอบคำถาม",
                      aliases=['ans'],
                      usage="<คำตอบ>",
                      )
    async def answer(self, ctx, *, answer=None): 
        if answer == None:
            await ctx.message.delete()
            await ctx.channel.send(f"โปรดป้อนคำตอบด้วยค่ะ", delete_after=10)
            return
        if not ctx.channel.id == 748537605389549629:
            await ctx.message.delete()
            await ctx.channel.send(f"โปรดป้อนคำตอบที่ห้อง <#748537605389549629> ด้วยค่ะ", delete_after=10)
            return

        db = cogs._json.read_json("user_data")

        if not await Quiz.is_reg(self, db, ctx.author): 
            await ctx.message.delete()
            await ctx.channel.send(f"โปรดลงทะเบียนสมาชิกก่อนนะคะ", delete_after=10)
            return

        uaid = str(ctx.author.id) # จะใช้ id ของ user เข้าถึงข้อมูล

        ql = cogs._json.read_json("quiz_list")
        qc = cogs._json.read_json("quiz_config")

        if qc['now'] is None: # None is null / null is None
            await ctx.message.delete()
            await ctx.author.send(f"ไม่มีคำถามที่ต้องตอบในเวลานี้ค่ะ", delete_after=10)
            return

        if db[uaid]['qtime'] == qc['qtime']:
            await ctx.message.delete()
            await ctx.author.send(f"ท่านได้ตอบคำถามรอบนี้ไปแล้วค่ะ", delete_after=10)

        quiz = ql[str(qc['now'])] # ดึงคำถามที่ใช้งานอยู่

        if answer in quiz['answer']:  # ตรวจสอบว่าสิ่งที่ตอบมานั้น อยู่ในคำตอบที่ถูกต้องหรือไม่
            
            
            db[uaid]['xp'] += int(quiz['xp'])
            db[uaid]['point'] += int(quiz['point'])
            db[uaid]['qtime'] = int(qc['qtime']) # จะเป็นการยืนยันว่า ได้ตอบคำถามรอบนี้ไปแล้ว
            cogs._json.write_json(db, "user_data")
            await ctx.message.delete()
            await ctx.author.send(f"ยินดีด้วยค่ะ ท่านตอบคำถามข้อนี้ถูกต้อง ได้รับ {quiz['xp']} xp และ {quiz['point']} point ค่ะ")

        else: # กรณีตอบไม่ถูก สามารถตอบใหม่ได้ ในตอนนี้น่ะนะ 555+
            await ctx.message.delete()
            await ctx.author.send(f"เสียใจด้วยค่ะ ท่านตอบคำถามข้อนี้ไม่ถูกต้องค่ะ")

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
    bot.add_cog(Quiz(bot))


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
