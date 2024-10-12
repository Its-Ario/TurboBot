import bale
import balethon
import aiohttp
import requests 
import json
import os
import database
import random
import hashlib

import balethon.objects
import balethon.conditions
import balethon.event_handlers

ai_chat = 15
logo_make = 20
image_gen = 20
font_maker = 10
tts = 15

vsite = ""
adminpass = 123456789

token = "1564793598:56MkimbBB3p1HyjuHBAZCppgdL5UDx4Q8iNtVbXO"

owner = 429632558
developer = 2089986546
admins = [owner , developer]

client_bt = balethon.Client(token)
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
            t.add(bale.InlineKeyboardButton(x[0],callback_data=x[1]),dx)
        dx += 1
    return t

join_channels = []
with open("joins.json", "r") as f:
    join_channels = json.load(f)


@client.event
async def on_ready():
    print(f"Logged in as {client.user.username}")
    await client.send_message(developer, f"🛡️ Logged in as @{client.user.username} at state {'*dev mode*' if develop_mode else '*public mode*'}\n[✅ start the bot](send:/start)")
    #await client.send_message(owner, f"🛡️ Logged in as @{client.user.username} at state {'*dev mode*' if develop_mode else '*public mode*'}")


@client.event
async def on_message(message:bale.Message):
    if develop_mode and message.author.id != developer : return print(f"DEVMODE : {message.author.id} - {message.content}")
    text = message.content
    m = message
    user = message.author
    if str(user.id) in state.keys():return
    if str(user.id) not in state.keys():
        database.create_database()
        db = database.read_database()
        if str(user.id) not in db.keys():
            db[str(user.id)] = {
                "uid": str(user.id),
                "username": str(user.username),
                "coins": 15,
            }
            database.write_database(db)
            await client.send_message(user.id,"🤩 سلام عزیزم! به بات خوش اومدی! چون اولین باره باتو استارت میزنی، بهت 15 تا سکه دادم! برو عشق کن")
        if text == "/start" or text == "🏠 بازگشت":
            await client.forward_message(message.chat.id,1386783796,55)
            keyboard = torow(
                [("🤖 هوش مصنوعی"), ("🐍 بازی و دریافت سکه")],
                [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                [("👤 پشتیبانی"),("👤 حساب کاربری")]
            )
            await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
        
        elif text == "🐍 بازی و دریافت سکه":
            URL = "https://tanjiro-bale-bot.vercel.app/?hash={hash}"
            
            user_id = str(m.author.id)
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()
            
            return await m.reply(URL.format(hash=user_hash))
            
        elif text == "score":
            URL = "https://127.0.0.1:443/get-score?hash={hash}"
            
            user_id = str(m.author.id)
            user_hash = hashlib.sha256(user_id.encode()).hexdigest()
            
            data = requests.get(URL.format(hash=user_hash), verify=False).json()
            print(data)
            return await m.reply(f"Score: {data["score"]}")

        
        elif text == "🤖 هوش مصنوعی":
            db = database.read_database()
            if db[str(user.id)]["coins"] < ai_chat:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر",components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            else:
                await m.reply("🤖 لطفا متن خود را بنویسید",components=torow(
                    [("🏠 بازگشت")]
                ))
                state[str(user.id)] = "ai_chats"
                def answer_checker(m:bale.Message):
                    return m.author.id == user.id and bool(m.text)
                text = await client.wait_for("message",check=answer_checker)
                if text == "/start" or text == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🤖 هوش مصنوعی"), ("🐍 بازی و دریافت سکه")],
                        [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
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
                await m.reply("💰 سکه شما کمه! برو سکه بگیر",components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await message.reply("🏞️ لطفا متن خود را بنویسید",components=torow(
                    [("🏠 بازگشت")]
                ))
            state[str(user.id)] = "logo_make"

        elif text == "🏞️ ساخت عکس":
            db  = database.read_database()
            if db[str(user.id)]["coins"] < image_gen:
                await m.reply("💰 سکه شما کمه! برو سکه بگیر",components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await m.reply("🏞️ لطفا متن خود را بنویسید",components=torow(
                    [("🏠 بازگشت")]
                ))
            def answer_checker(m:bale.Message):
                return m.author == user and bool(m.text)
            d = await client.wait_for("message",check=answer_checker)
            if d == "/start" or text == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🤖 هوش مصنوعی"), ("🐍 بازی و دریافت سکه")],
                        [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
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

            await m.reply(f"لطفاً متن مورد نظر خود را وارد کنید.\n```[حروف قابل استفاده]\nفارسی: {fa_chars_support}\nانگلیسی: {eng_chars_support}```")
            state[str(user.id)] = "font:wait_for_name"
            def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
            name = await client.wait_for("message", check=answer_checker)
            
            if name == "/start" or name == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🤖 هوش مصنوعی"), ("🐍 بازی و دریافت سکه")],
                        [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)

            if set(name.text).issubset(fa_chars):
                api_url = fa_api + name.text
                end_range = 10
                font_lang = "fa"
            elif set(name.text).issubset(eng_chars):
                api_url = eng_api + name.text
                end_range = 138
                font_lang = "en"
            else:
                await m.reply("خطا: لطفاً فقط از حروف فارسی یا فقط از حروف انگلیسی استفاده کنید.")
                
            
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
                await m.reply("💰 سکه شما کمه! برو سکه بگیر",components=torow(
                    [("🏠 بازگشت")]
                ))
                return
            await m.reply("لطفاً متن مورد نظر خود را وارد کنید.")
            state[str(user.id)] = "text_to_voice:wait_for_name"
            def answer_checker(msg: bale.Message):
                return msg.author == user and bool(msg.text)
            name = await client.wait_for("message", check=answer_checker)
            if name == "/start" or name == "🏠 بازگشت":
                    await client.forward_message(message.chat.id,1386783796,55)
                    keyboard = torow(
                        [("🤖 هوش مصنوعی"), ("🐍 بازی و دریافت سکه")],
                        [("📷 ساخت لوگو") , ("🏞️ ساخت عکس")],
                        [("✏️ ساخت فونت"),("🔊 متن به صدا")],
                        [("👤 پشتیبانی"),("👤 حساب کاربری")]
                    )
                    await client.send_message(user.id, "من چه کاری میتونم برات انجام بدم؟", components=keyboard)
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
            
            

        elif text == "👤 پشتیبانی":

            await client.send_message(user.id,"آیدی مالک بات جهت پشتیبانی: @admin_turbo", components=None)

        elif text == "👤 حساب کاربری":
            db = database.read_database()
            text = f"""\
✏️ حساب شما »
🆔 آیدی عددی: {user.id}
👤 نام کاربری: @{user.username}
💰 سکه‌های شما: {db[str(user.id)]["coins"]}
    """
            await client.send_message(user.id, text, components=torow(
                [("🏠 بازگشت")]
            ))
        
        elif (text == "/admin" or text == "/panel") and user.id in admins:
            if develop_mode == True:
                keyboard = torowinline(
                    [("🛡️ تعداد اعضا","users")],
                    [("🛡️ ارسال پیام به همه","sta")],
                    [("🛡️ ارسال سکه به همه","add_cta")],
                    [("🛡️ ارسال سکه به یک شخص","add_cta_one")],
                    [("🛡️ ارسال پیام به یک شخص","sta_one")],
                    [("❌ غیرفعال سازی حالت شخصی","dev_mode:off")],
                    [("👤 سایت پنل مدیریت","panel")]
                )

                await client.send_message(user.id,"دستورات مدیریتی",components=keyboard)
            else:
                keyboard = torowinline(
                    [("🛡️ تعداد اعضا","users")],
                    [("🛡️ ارسال پیام به همه","sta")],
                    [("🛡️ ارسال سکه به همه","add_cta")],
                    [("🛡️ ارسال سکه به یک شخص","add_cta_one")],
                    [("🛡️ ارسال پیام به یک شخص","sta_one")],
                    [("✅ فعال سازی حالت شخصی","dev_mode:on")],
                    [("👤 سایت پنل مدیریت","panel")]
                )

                await client.send_message(user.id,"دستورات مدیریتی",components=keyboard)
    
    if state.get(str(user.id)) == "ai_chat":
        if text == "🏠 بازگشت":
            await client.send_message(user.id, "بازگشت به منو",components=torow(
                [("🤖 هوش مصنوعی")],
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
                [("🤖 هوش مصنوعی")],
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
                    data = await response.content.read()
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
        await m.reply(f"تعداد کاربران: {len(db.keys())}")

    elif query == "sta":
        users = database.read_database().keys()
        await sm(user.id,"✏️ متن پیام خود را بفرستید\n[لغو](send:لغو)")
        state[str(user.id)] = "sta"
        def answer_checker(m:bale.Message):
            return m.author == user and bool(m.text)
        answer = await client.wait_for("message",check=answer_checker)
        
        
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
                try:
                    await client.send_message(x,answer.text)
                    sended += 1
                except:
                    failed += 1
                await m.edit(sf())
        
    elif query == "add_cta":
        pass

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
        await sm(s,"💰 ادمین بهت {0} پول داد".format(answer.text))

    elif query == "sta_one":
        db = database.read_database().keys()
        await m.reply("آیدی عددی کاربر را بفرستید")
        state[str(user.id)] = "sta_one"
        def answer_checker(m:bale.Message):
            return m.author == user and bool(m.text)
        answer = await client.wait_for("message",check=answer_checker)
        try:
            int(answer.text)
            del state[str(user.id)]
        except:
            await m.reply("آیدی صحیح نیست",components=torowinline(
                [
                    ("تلاش مجدد","sta_one")
                ]
            ))

    elif query == "dev_mode:off":
        develop_mode = False
        await m.reply("میتوانید به صورت عادی از بات استفاده کنید")

    elif query == "dev_mode:on":
        develop_mode = True
        await m.reply("DEVELOP MODE فعال شد. فقط ادمین ها میتوانند از بات استفاده کنند")

    elif query == "panel":
        text =  f"""\
{vsite}/panel?pass={user.id}{adminpass}
"""
        await m.reply(text)
        
async def sendGameMessage(data):
    print(data)

    


client.run()