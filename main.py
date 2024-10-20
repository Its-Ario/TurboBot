import bale
import aiohttp
import json
import database
import random
import hashlib
import re
import time

from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

from esmfamil import alphabetList, formatResponse

ai_chat = 10
logo_make = 15
image_gen = 15
font_maker = 10
tts = 10
esmfamil = 10
mvs = 5

vsite = ""
adminpass = 123456789

token = "1564793598:56MkimbBB3p1HyjuHBAZCppgdL5UDx4Q8iNtVbXO"

client = bale.Bot(token)

develop_mode = False

state = {}

def torow(*row:list):
    t = bale.MenuKeyboardMarkup()
    dx = 1
    for item in row:
        for x in item:
            t.add(bale.MenuKeyboardButton(x),dx)
        dx += 1
    return t

def torowinline(*row:list):
    t = bale.InlineKeyboardMarkup()
    dx = 1
    for item in row:
        for x in item:
            if x[1].startswith("URL:"):
                t.add(bale.InlineKeyboardButton(x[0],url=x[1].removeprefix("URL:")),dx)
            else: t.add(bale.InlineKeyboardButton(x[0],callback_data=x[1]),dx)
        dx += 1
    return t

async def checkChannels(message:bale.Message):
    verified = True
    join_channels = []
    with open("Data/data.json", "r") as f:
        join_channels = json.load(f)["joins"]
        channels = {}
        for channel in join_channels:
            try:
                chat = await client.get_chat(channel)
                user = await client.get_user(message.author.id)
                await chat.get_chat_member(user)
                        
            except bale.error.BadRequest as e:
                if e.message == "Bad Request: message not found":
                    verified = False
                    channels[channel] = f"URL:https://{chat.invite_link}"
            except Exception as e:
                logger.error(e)
    
    if not verified:        
        try:
            lst = [[(f"کانال اسپانسر {cnt+1}", url)] for cnt, url in enumerate(channels.values())]

            await message.reply(
                """*سلام😉
برای استفاده از ربات اول در کانال های زیر عضو شوید👇
و بعد روی دکمه ی [استارت](send:/start)  بزنید❤️
تا ربات شروع به کار کند❤️‍🔥*""", 
                components=torowinline(*lst)
            )
        except Exception as e: logger.error(e)
    
    return verified

async def verifyUser(id:str) -> bale.User:
    try:
        user = await client.get_user(id)
        if not user: return False
        return user
    except:
        return False


@client.event
async def on_ready():
    logger.info(f"Logged in as {client.user.username}")

@client.event
async def on_message(message:bale.Message):
    if not message.author: return
    
    text = message.content
    m = message
    user = message.author
    if not await checkChannels(m): return
    if str(user.id) in state.keys():return
    if str(user.id) not in state.keys():
        database.create_database()
        db = database.read_database()

        if str(user.id) not in db.keys():
            inviter = text.removeprefix("/start _ref_")
            u = await verifyUser(inviter)
            if inviter == text or not u or inviter == str(user.id):
                inviter = None
            db[str(user.id)] = {
                "uid": str(user.id),
                "username": str(user.username),
                "coins": 15,
                "inviter": inviter,
                "invited": 0
            }
            if u:
                db[str(u.id)]["coins"] += 10
                db[str(u.id)]["invited"] += 1
                
            database.write_database(db)
            await client.send_message(user.id,"🤩 سلام عزیزم! به بات خوش اومدی! چون اولین باره باتو استارت میزنی، بهت 15 تا سکه دادم! برو عشق کن")
        if text.startswith("/start") or text == "🏠 بازگشت":
            await client.forward_message(message.chat.id,1386783796,55)
            keyboard = torow(
                [("🐍 بازی و دریافت سکه")],
                [("🤖 هوش مصنوعی")],
                [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                [("👤 پشتیبانی"),("👤 حساب کاربری")]
            )
            return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
        
        elif text == "🐍 بازی و دریافت سکه":
            URL = "http://5.10.249.8:5000/?hash={hash}"
            
            user_id = str(m.author.id)
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()
            
            formmated_url = URL.format(hash=user_hash)
            
            return await m.reply("🐍 برای بازی و دریافت سکه روی لینک زیر کلیک کنید!",components=torowinline(
                [("شروع بازی", f"URL:{formmated_url}")],
                [("برداشت سکه", f"getscore_{user_id}")]
            ))

        
        elif text == "🤖 هوش مصنوعی":
            db = database.read_database()
            if db[str(user.id)]["coins"] < ai_chat:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=ai_chat),components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            else:
                await m.reply("🤖 لطفا متن خود را بنویسید"
                            "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=ai_chat),components=torow(
                    [("🏠 بازگشت")]
                ))
                state[str(user.id)] = "ai_chats"
                def answer_checker(m:bale.Message):
                    return m.author.id == user.id and bool(m.text)
                text = await client.wait_for("message",check=answer_checker)
                if text.content == "/start" or text.content == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🐍 بازی و دریافت سکه")],
                        [("🤖 هوش مصنوعی")],
                        [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                        [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    del state[str(user.id)]
                    return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
                
                wait_message = await m.reply("لطفا صبر کنید...")
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://heroapi.ir/api/duckduckgo/chat?query={text.text}&model=gpt-4o-mini&timeout=30') as response:
                        result = await response.json()
                        await wait_message.edit(result["message"])
                        db[str(user.id)]["coins"] -= ai_chat
                        database.write_database(db)
                        del state[str(user.id)]

        elif text == "📷 ساخت لوگو":
            db = database.read_database()
            if db[str(user.id)]["coins"] < logo_make:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=logo_make),components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await message.reply("🏞️ لطفا متن خود را بنویسید"
                            "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=logo_make),components=torow(
                    [("🏠 بازگشت")]
                ))
            state[str(user.id)] = "logo_make"

        elif text == "🏞️ ساخت عکس":
            db  = database.read_database()
            if db[str(user.id)]["coins"] < image_gen:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=image_gen),components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await m.reply("🏞️ لطفا متن خود را بنویسید"
                            "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=image_gen),components=torow(
                    [("🏠 بازگشت")]
                ))
            
            def answer_checker(m:bale.Message):
                return m.author == user and bool(m.text)
            d = await client.wait_for("message",check=answer_checker)
            if d.text == "/start" or d.text == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🐍 بازی و دریافت سکه")],
                        [("🤖 هوش مصنوعی")],
                        [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                        [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
            api_img = "https://heroapi.ir/api/lexica?query="+d.text
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_img) as resp:
                        if resp.status == 200:
                            link = await resp.json()
                            img_url = random.choice(link.get("images"))["src"]
                            async with aiohttp.ClientSession() as session:
                                async with session.get(img_url) as resp:
                                    if resp.status == 200:
                                        data = await resp.read()

                                        data = bale.InputFile(data)
                                        await client.send_photo(user.id,photo=data,caption=f"🏞️ {d.text}",components=torow(
                                            [("🏠 بازگشت")]
                                        ))
            except:
                await m.reply("❌ خطا")
                    

        elif text == "✏️ ساخت فونت":
            db = database.read_database()
            if db[str(user.id)]["coins"] < font_maker:
                await m.reply("موجودی سکه شما کافی نیست. لطفاً سکه بیشتری دریافت کنید.",components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            
            eng_api = "https://api.codebazan.ir/font/?text="
            fa_api = "https://api.codebazan.ir/font/?type=fa&text="

            eng_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            fa_chars = set("آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی")


            fa_chars_support = ' , '.join(fa_chars)
            eng_chars_support = ' , '.join(eng_chars)

            await m.reply(f"لطفاً متن مورد نظر خود را وارد کنید.\n```[حروف قابل استفاده]\nفارسی: {fa_chars_support}\nانگلیسی: {eng_chars_support}```", components=torow(
                    [("🏠 بازگشت")]
                ))
            state[str(user.id)] = "font:wait_for_name"
            def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
            name = await client.wait_for("message", check=answer_checker)
            
            if name.content == "/start" or name.content == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🐍 بازی و دریافت سکه")],
                        [("🤖 هوش مصنوعی")],
                        [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                        [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    del state[str(user.id)]
                    return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)

            if set(name.text).issubset(fa_chars):
                api_url = fa_api + name.text
                end_range = 10
                font_lang = "fa"
            elif set(name.text).issubset(eng_chars):
                api_url = eng_api + name.text
                end_range = 138
                font_lang = "en"
            else:
                del state[str(user.id)]
                return await m.reply("خطا: لطفاً فقط از حروف فارسی یا فقط از حروف انگلیسی استفاده کنید.")
                
            
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        while True:
                            await m.reply(f'لطفاً یک شماره بین 1 تا {end_range} انتخاب کنید.')
                            state[str(user.id)] = "font:wait_for_number"
                            answer = await client.wait_for("message", check=answer_checker)
                            
                            persian_digits = '۰۱۲۳۴۵۶۷۸۹'
                            arabic_digits = '٠١٢٣٤٥٦٧٨٩'
                            english_digits = '0123456789'
                            translation_table = str.maketrans(persian_digits + arabic_digits, english_digits * 2)
                            translated_text = answer.text.translate(translation_table)
                            
                            if translated_text.isdigit():
                                number = int(translated_text)
                                if 1 <= number <= end_range:
                                    break
                                else:
                                    await m.reply(f"خطا: لطفاً عددی بین 1 و {end_range} وارد کنید.")
                                    del state[str(user.id)]

                            else:
                                await m.reply("خطا: لطفاً یک عدد معتبر وارد کنید.")
                                del state[str(user.id)]

                        
                        data = data['result' if font_lang == "en" else 'Result'][str(number)]
                        text = f"""
فونت مورد نظر شما با موفقیت ایجاد شد. ✅
توجه: {font_maker} سکه از حساب شما کسر شد. 💰

متن اصلی: {name.text} 📝
زبان: {"فارسی" if font_lang == "fa" else "انگلیسی"} 🌐
فونت ایجاد شده: {data} 🎨
```[برای کپی کردن فونت اینجا را لمس کنید]{data}```
"""
                        
                        keyboard = torow(
                            [("✏️ ساخت فونت"), ("🏠 بازگشت")]
                        )
                        
                                    
                        await m.reply(text, components=keyboard)
                        db = database.read_database()
                        db[str(user.id)]["coins"] -= font_maker
                        database.write_database(db)
                        try:
                            del state[str(user.id)]
                        except:
                            pass
                        return
                    else:
                        await m.reply("خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.",components=torow(
                            [("🏠 بازگشت")]
                        ))
                        try:
                            del state[str(user.id)]
                        except:
                            pass
                        return
            
        elif text == "🔊 متن به صدا":
            db = database.read_database()
            if db[str(user.id)]["coins"] < tts:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=tts),components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await m.reply("لطفاً متن مورد نظر خود را وارد کنید."
                            "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=tts),components=torow(
                    [("🏠 بازگشت")]
                            )
            )
            state[str(user.id)] = "text_to_voice:wait_for_name"
            def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
            name = await client.wait_for("message", check=answer_checker)
            if name.content == "/start" or name.content == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🐍 بازی و دریافت سکه")],
                        [("🤖 هوش مصنوعی")],
                        [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                        [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    del state[str(user.id)]
                    return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
            api_url = f"https://api.irateam.ir/create-voice/?text={name.text}&Character=FaridNeural"
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as resp:
                    if resp.status == 200:
                        link = await resp.json()
                                                
                        async with aiohttp.ClientSession() as session:
                            async with session.get(link["results"].get("url")) as resp:
                                data = await resp.read()
                                
                                await client.send_audio(m.chat_id, bale.InputFile(data, file_name="Audio.mp3"),caption="صوت شما ساخته شد" , reply_to_message_id=m._id)
                        try:
                            del state[str(user.id)]
                        except:
                            pass
                        
                        db[str(user.id)]["coins"] -= tts
                        return database.write_database(db)
                    else:
                        await m.reply("خطا در دریافت اطلاعات. لطفاً دوباره تلاش کنید.",components=torow(
                            [("🏠 بازگشت")]
                        ))
                        try:
                            del state[str(user.id)]
                        except:
                            pass
                        return
                    
        elif text == "😜 تقلب اسم فامیل":
            await message.reply("🔠 حرف موردنظر را انتخاب کنید:"
                                "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=esmfamil), components=alphabetList())
            
        elif text == "🎞 جست و جوی فیلم":
            state[str(user.id)] = "mvs"
            db = database.read_database()
            if db[str(user.id)]["coins"] < mvs:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=mvs),components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await message.reply("لطفا نام فیلم موردنظر را وارد کنید:"
                                "\n💸 هر استفاده از این بخش {coin} سکه میخواد!".format(coin=mvs), components=torow(
                    [("🏠 بازگشت")]
                ))
            def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
            name = await client.wait_for("message", check=answer_checker)
            if name.content == "/start" or name.content == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🐍 بازی و دریافت سکه")],
                        [("🤖 هوش مصنوعی")],
                        [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
                        [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    del state[str(user.id)]
                    return await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
            sk = re.sub(r'\s+', ' ', name.content).strip()
            async with aiohttp.ClientSession() as session:
                try:
                    url = f"https://www.omdbapi.com/?t={sk}&apikey=e430f1ee"
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json()
                        if data["Response"] == "False":
                            return await message.reply("❌ فیلم پیدا نشد!", components=torow(
                            [("🏠 بازگشت")]
                        ))
                        await message.reply(
                            f"🎬 نام: {data['Title']}\n"
                            f"📅 سال تولید: {data['Year']}\n"
                            f"⭐ امتیاز: {data['Rated']}\n"
                            f"🎞️ ژانر: {data['Genre']}\n"
                            f"🎥 کارگردان: {data['Director']}\n"
                            f"👥 بازیگران: {data['Actors']}", components=torow(
                            [("🏠 بازگشت")]
                        ))
                        db[str(user.id)]["coins"] -= mvs
                except Exception:
                    return await message.reply("❌ خطا!", components=torow(
                            [("🏠 بازگشت")]
                        ))
            try:
                del state[str(user.id)]
            except: ...

        elif text == "👤 پشتیبانی":

            await client.send_message(user.id,"آیدی مالک بات جهت پشتیبانی و خرید سکه👨‍💻👇 @admin_turbo", components=torow(
                            [("🏠 بازگشت")]
                        ))

        elif text == "👤 حساب کاربری":
            db = database.read_database()
            text = f"""\
✏️ حساب شما »
🆔 آیدی عددی: {user.id}
👤 نام کاربری: @{user.username}
💰 سکه‌های شما: {db[str(user.id)]["coins"]}
👥 افراد دعوت شده: {db[str(user.id)]["invited"]}
    """
            await client.send_message(user.id, text, components=torowinline(
                [("💰 دعوت دیگران", "banner")],
                [("🏠 بازگشت", "return")]
            ))
        
        elif (text == "/admin" or text == "/panel"):
            with open("Data/data.json", "r") as f:
                admins:list = json.load(f)["admins"]
            if user.id not in admins: return
            
            keyboard = torowinline(
                [("🛡️ تعداد اعضا","users")],
                [("🛡️ ارسال پیام به همه","sta")],
                [("🛡️ ارسال سکه به همه","add_cta")],
                [("🛡️ ارسال سکه به یک شخص","add_cta_one")],
                [("🛡️ اضافه کردن کانال", "cha_add")],
                [("🛡️ حذف کانال", "cha_del")],
                [("🛡️ لیست کانال ها", "cha_list")],
                [("🛡️ اضافه کردن ادمین", "admin_add")],
                [("🛡️ حذف ادمین", "admin_del")],
                [("🛡️ لیست ادمین", "admin_list")]
                # [("👤 سایت پنل مدیریت","panel")]
            )

            await client.send_message(user.id,"دستورات مدیریتی",components=keyboard)
    
    if state.get(str(user.id)) == "ai_chat":
        if text == "🏠 بازگشت":
            await client.send_message(user.id, "بازگشت به منو",components=torow(
                [("🤖 هوش مصنوعی"), ("😜 تقلب اسم فامیل")],
                [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                [("✏️ ساخت فونت")],
                [("🔊 متن به صدا")],
                [("👤 پشتیبانی"),("👤 حساب کاربری")]
            ))
            del state[str(user.id)]
        else:
            db = database.read_database()
            ai_api = "https://api-free.ir/api/bard.php?text="+text
            async with aiohttp.ClientSession() as session:
                async with session.get(ai_api) as response:
                    data = await response.json()
                    M = data["result"]
                    await m.reply(
                        M,
                        components=torow(
                            [("🏠 بازگشت")]
                        )
                    )
                    db[str(user.id)]["coins"] -= ai_chat
                    database.write_database(db)
                    del state[str(user.id)]
    elif state.get(str(user.id)) == "logo_make":
        def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
        ans = await client.wait_for("message",check=answer_checker)
        ans = ans.content
        if text == "🏠 بازگشت":
            await client.send_message(user.id, "بازگشت به منو",components=torow(
                [("🤖 هوش مصنوعی"), ("😜 تقلب اسم فامیل")],
                [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                [("✏️ ساخت فونت")],
                [("🔊 متن به صدا")],
                [("👤 پشتیبانی"),("👤 حساب کاربری")]
            ))
            del state[str(user.id)]
        else:
            scripts = ['neon-logo', 'booking-logo', 'comics-logo', 'water-logo', 'fire-logo', 'clan-logo', 'my-love-logo', 'blackbird-logo', 'smurfs-logo', 'style-logo', 'runner-logo', 'fluffy-logo', 'glow-logo', 'crafts-logo', 'fabulous-logo', 'amped-logo', 'graffiti-logo', 'graffiti-burn-logo', 'star-wars-logo', 'graffiti-3d-logo', 'scribble-logo', 'chrominium-logo', 'harry-potter-logo', 'world-cup-2014-logo', 'heavy-metal-logo', 'thanksgiving1-logo', 'april-fools-logo', 'beauty-logo', 'winner-logo', 'silver-logo', 'steel-logo', 'global-logo', 'inferno-logo', 'birdy-logo', 'roman-logo', 'minions-logo', 'superfit-logo', 'fun-and-play-logo', 'brushed-metal-logo', 'birthday-fun-logo', 'colored2-logo', 'swordfire-logo', 'flame-logo', 'wild-logo', 'street-sport-logo', 'surfboard-white-logo', 'amazing-3d-logo', 'flash-fire-logo', 'uprise-logo', 'sugar-logo', 'robot-logo', 'genius-logo', 'cereal-logo', 'kryptonite-logo', 'patriot-logo', 'holiday-logo', 'sports-logo', 'thanksgiving2-logo', 'trance-logo', 'spider-men-logo', 'theatre-logo', 'vintage-racing-logo', 'ninja-logo', 'bumblebee-logo', 'vampire-logo', 'sunrise-logo', 'monsoon-logo', 'strongman-logo', 'game-over-logo']
            if len(ans) >= 50:
                return await client.send_message(user.id, "متن بیشتر از 50 کاراکتر نمیتواند باشد")
            api = "https://api.irateam.ir/Logo-Maker/?script="+random.choice(scripts)+"&fontsize=200&textcolor=red&text="+ans.replace(" ","")
            async with aiohttp.ClientSession() as session:
                async with session.get(api) as response:
                    data = await response.read()
                    await client.send_photo(user.id, bale.InputFile(data), caption="لوگو شما ساخته شد",components=torow(
                        [("🏠 بازگشت")]
                    ))
                    db = database.read_database()
                    db[str(user.id)]["coins"] -= logo_make
                    database.write_database(db)
                    del state[str(user.id)]
@client.event
async def on_callback(callback_query:bale.CallbackQuery):
    query = callback_query.data
    m = callback_query.message
    user = callback_query.user
    sm = client.send_message
    
    if query == "users":
        db = database.read_database()
        await m.reply(f"تعداد کاربران: {len([user for user in db.keys() if str(user).isalnum()])}")

    elif query == "sta":
        users = database.read_database().keys()
        await sm(user.id,"✏️ متن پیام خود را بفرستید\n[لغو](send:لغو)")
        state[str(user.id)] = "sta"
        def answer_checker(m:bale.Message):
            return m.author == user and (bool(m.text) or bool(m.caption))
        answer = await client.wait_for("message",check=answer_checker)
        
        fw = False
        if answer.forward_from:
            fw = True
                    
        if answer.attachment:
            img = answer.attachment.to_input_file()
        else: img = None
        
        sended = 0
        failed = 0
        def sf():
            return f"""\
        👤 تعداد کل کاربران : {len(users)}
        ✅ تعداد ارسال شده : {sended}
        ❌ تعداد ارسال نشده : {failed}
        ✏️ تعداد کل پیام ها : {sended+failed}
        """
        if answer.text == "لغو":
            await m.reply("لغو شد") 
            del state[str(user.id)]
            return await m.reply("بازگشت به پنل",components=torow([("/admin")]))
        
        else:
            m = await sm(user.id,sf())
            for x in users:
                if not str(x).isalnum(): continue
                try:
                    if fw:
                        await client.forward_message(x, answer.chat_id, answer._id)
                    elif img:
                        await client.send_photo(x, img, caption=answer.caption)
                    else: await client.send_message(x,answer.text)
                    sended += 1
                except:
                    failed += 1
                await m.edit(sf())
        
    elif query == "add_cta":
        users = database.read_database().keys()
        await sm(user.id,"✏️ مقدار سکه موردنظر را ارسال کنید\n[لغو](send:لغو)")
        state[str(user.id)] = "add_cta"
        def answer_checker(m:bale.Message):
            return m.author == user and bool(m.text)
        answer = await client.wait_for("message",check=answer_checker)
        if not answer.text.isnumeric():
            return await m.reply("ورودی نامتعبر")
        db = database.read_database()
        
        coin_msg = "💰 ادمین بهت *{0}* سکه داد".format(answer.text)
        
        sended = 0
        failed = 0
        def sf():
            return f"""\
👤 تعداد کل کاربران : {len(users)}
✅ تعداد ارسال شده : {sended}
❌ تعداد ارسال نشده : {failed}
✏️ تعداد کل پیام ها : {sended+failed}
"""
        if answer.text == "لغو":
            await m.reply("لغو شد")
            del state[str(user.id)]
            return await m.reply("بازگشت به پنل",components=torow([("/admin")]))
        
        else:
            m = await sm(user.id,sf())
            for x in users:
                if not str(x).isalnum(): continue
                try:
                    db[str(user.id)]["coins"] += int(answer.text)
                    await client.send_message(x,coin_msg)
                    sended += 1
                except:
                    failed += 1
                await m.edit(sf())
    
    elif query.startswith("getscore"):
        db = database.read_database()
        URL = "http://5.10.249.8:5000/get-score?hash={hash}"

        user_id = query.removeprefix("getscore_")
        user_hash = hashlib.sha256(user_id.encode()).hexdigest()

        async with aiohttp.ClientSession() as session:
            async with session.get(URL.format(hash=user_hash)) as response:
                data = await response.json()

        if data.get("ok"):
            score = data["score"]
            db[str(user.id)]["coins"] += score
            database.write_database(db)
            return await m.reply(f"شما *{score}* سکه از بازی بدست آوردید!")
        
        if data.get("error") == "User hash not found":
            return await m.reply("سکه ای برای شما ثبت نشده!")

    elif query == "add_cta_one":
        
        await m.reply("آیدی عددی یا حروفی کاربر را بفرستید")
        state[str(user.id)] = "add_cta"
        def answer_checker(m:bale.Message):
            return m.author == user and bool(m.text)
        answer = await client.wait_for("message",check=answer_checker)
        while True:
            try:
                s = await client.get_user(answer.text)
                s = s.id

                del state[str(user.id)]
                break
            except:
                await m.reply("آیدی صحیح نیست\nآیدی عددی یا حروفی کاربر را بفرستید\n[لغو](send:لغو)")
                answer = await client.wait_for("message",check=answer_checker)
                if answer == "لغو":
                    await m.reply("لغو شد")
                    del state[str(user.id)]
                    return await m.reply("بازگشت به پنل",components=torow([("/admin")]))
            
        await m.reply("تعداد پولی که میخواهید به کاربر اضافه کنید را بفرستید")
        state[str(user.id)] = "add_cta"
        def answer_checker(m:bale.Message):
            return m.author == user and bool(m.text)
        answer = await client.wait_for("message",check=answer_checker)

        while True:
            try:
                int(answer.text)
                del state[str(user.id)]
                break
            except:
                await m.reply("تعداد پولی که میخواهید به کاربر اضافه کنید را به صورت عددی بفرستید\n[لغو](send:لغو)")
                answer = await client.wait_for("message",check=answer_checker)
                if answer == "لغو":
                    await m.reply("لغو شد")
                    del state[str(user.id)]
                    return await m.reply("بازگشت به پنل",components=torow([("/admin")]))
        db = database.read_database()
        db[str(s)]["coins"] += int(answer.text)
        database.write_database(db)
        await m.reply("کاربر با موفقیت آپدیت شد")
        await sm(s,"💰 ادمین بهت {0} سکه داد".format(answer.text))

    elif query.startswith("cha"):
        clean = query.removeprefix("cha_")
        if clean == "add":
            state[str(user.id)] = "cha_add"
            with open("Data/data.json", "r") as f:
                current_data:list = json.load(f)
                
            await m.reply("Enter Channel ID:")
            def answer_checker(m:bale.Message):
                return m.author.id == user.id and bool(m.text)
            text = await client.wait_for("message",check=answer_checker)
            
            if not text.content.isnumeric():
                del state[str(user.id)]
                return await text.reply("Invalid ID!")
            
            if text.content in current_data["joins"]:
                del state[str(user.id)]
                return await text.reply("Channel Already Added!")
                
            current_data["joins"].append(text.content)
            
            with open("Data/data.json", "w") as f:
                json.dump(current_data, f)
                
            await text.reply(f"Added Channel {text.content}")
            del state[str(user.id)]
        elif clean == "del":
            state[str(user.id)] = "cha_del"
            
            with open("Data/data.json", "r") as f:
                current_data:list = json.load(f)
                
            await m.reply("Enter Channel ID:")
            def answer_checker(m:bale.Message):
                return m.author.id == user.id and bool(m.text)
            text = await client.wait_for("message",check=answer_checker)
            
            if text.content not in current_data["joins"]:
                del state[str(user.id)]
                return await text.reply("Channel Not In Database!")
            
            current_data["joins"].remove(text.content)
            
            with open("Data/data.json", "w") as f:
                json.dump(current_data, f)
                
            await text.reply(f"Removed Channel {text.content}")
            del state[str(user.id)]
            
        elif clean == "list":
            state[str(user.id)] = "cha_list"
            
            with open("Data/data.json", "r") as f:
                current_data:list = json.load(f)
            
            msg = ""
            for channel_id in current_data["joins"]:
                try:
                    chat = await client.get_chat(channel_id)
                    msg += f"- [{chat.title}](https://{chat.invite_link}) ({f"{chat.username}, {channel_id}"})\n"
                except bale.error.BadRequest as e:
                    if e.message == "Bad Request: message not found":
                        msg += f"- _Invalid Channel_ ({channel_id})\n"
                        
            if not msg:
                msg = "No Channels Found!"
                        
            await m.reply(msg)
            
    elif query.startswith("admin"):
        clean = query.removeprefix("admin_")
        if clean == "add":
            state[str(user.id)] = "admin_add"
            with open("Data/data.json", "r") as f:
                current_data:list = json.load(f)
                
            await m.reply("Enter User ID:")
            def answer_checker(m:bale.Message):
                return m.author.id == user.id and bool(m.text)
            text = await client.wait_for("message",check=answer_checker)
            
            if not text.content.isnumeric():
                del state[str(user.id)]
                return await text.reply("Invalid ID!")
            
            if text.content in current_data["admins"]:
                del state[str(user.id)]
                return await text.reply("Admin Already Added!")
                
            current_data["admins"].append(text.content)
            
            with open("Data/data.json", "w") as f:
                json.dump(current_data, f)
                
            await text.reply(f"Added Admin {text.content}")
            del state[str(user.id)]
        elif clean == "del":
            state[str(user.id)] = "admin_del"
            
            with open("Data/data.json", "r") as f:
                current_data = json.load(f)
                
            await m.reply("Enter User ID:")
            def answer_checker(m:bale.Message):
                return m.author.id == user.id and bool(m.text)
            text = await client.wait_for("message",check=answer_checker)
            
            if text.content not in map(str, current_data["admins"]):
                del state[str(user.id)]
                return await text.reply("User Not In Database!")
            
            current_data["admins"].remove(text.content)
            
            with open("Data/data.json", "w") as f:
                json.dump(current_data, f)
                
            await text.reply(f"Removed Admin {text.content}")
            del state[str(user.id)]
            
        elif clean == "list":
            state[str(user.id)] = "admin_list"
            
            with open("Data/data.json", "r") as f:
                current_data:list = json.load(f)
            
            msg = ""
            for user_id in current_data["admins"]:
                try:
                    chat = await client.get_user((str(user_id)))
                    if not chat: 
                        msg += f"- _Invalid User_ ({user_id})\n"
                    else:
                        msg += f"- {chat.first_name} ({f"{chat.username}, {user_id}"})\n"
                except bale.error.BadRequest as e:
                    if e.message == "Bad Request: message not found":
                        msg += f"- _Invalid User_ ({user_id})\n"
                        
            if not msg:
                msg = "No Admins Found!"
                        
            await m.reply(msg)
            
    elif query == "return":
        await client.forward_message(m.chat.id,1386783796,55)
        keyboard = torow(
            [("🐍 بازی و دریافت سکه")],
            [("🤖 هوش مصنوعی")],
            [("📷 ساخت لوگو"), ("😜 تقلب اسم فامیل")],
            [("🎞 جست و جوی فیلم") , ("🏞️ ساخت عکس")],
            [("✏️ ساخت فونت"),("🔊 متن به صدا")],
            [("👤 پشتیبانی"),("👤 حساب کاربری")]
        )
        await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
        
    elif query == "banner":
        bannerImg = "./Assets/bannerImg.jpg"
        linkTxt = f"ble.ir/{(await client.get_me()).username}?start=_ref_{user.id}"
        
        bannerTxt = """*سلام من تانجیرو هستم❤️‍🔥
برترین ربات بله💯

{link}

بیا استارت کن و چند تا از قابلیتام رو ببین👆🥰*"""

        with open(bannerImg, "rb") as img:
            inpFile = bale.InputFile(img.read())
            
        await m.reply_photo(inpFile, caption=bannerTxt.format(link=linkTxt))
        await client.send_message(m.chat_id, "*شما با دعوت هر نفر با بنر بالا 10 سکه دریافت میکنید😍*")
        
    elif query.startswith("esmfamil:"):
        letter = query.removeprefix("esmfamil:")
        db = database.read_database()
        
        url = f"https://api.codebazan.ir/esm-famil/?text={letter}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        formatted_message = formatResponse(content.decode())
                        if db[str(user.id)]["coins"] < esmfamil:
                            await m.reply("💰 سکه شما کمه! برو سکه بگیر"
                                            "\nشما برای استفاده از این بخش {coin} سکه نیاز دارید!".format(coin=esmfamil),components=torow(
                                [("🏠 بازگشت")]
                            ))
                            return
                        db[str(user.id)]["coins"] -= esmfamil
                        database.write_database(db)
                        return await m.reply(formatted_message, components=torow(
                            [("🏠 بازگشت")]
                        ))
                        
                    return await m.reply("❌ خطا!", components=torow(
                    [("🏠 بازگشت")]
                ))
            except KeyError as e:
                logger.error(e)
                return await m.reply("❌ خطا!", components=torow(
                    [("🏠 بازگشت")]
                ))
                        


if __name__ == "__main__":
    while True:
        try:
            client.run()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot is stopping...")
            break
        except Exception as e:
            logger.error(f"Bot crashed due to an error: {e}. Restarting in 5 seconds...")
            time.sleep(5)