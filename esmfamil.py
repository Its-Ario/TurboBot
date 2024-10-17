from bale import InlineKeyboardButton, InlineKeyboardMarkup
import re

def formatResponse(data):
    sections = {
        "اسم": "🎤",
        "فامیل": "👥",
        "شهر": "🌍",
        "کشور": "🇮🇷",
        "میوه": "🍉",
        "غذا": "🍲",
        "رنگ": "🎨",
        "حیوان": "🐴",
        "ماشین": "🚗",
        "اشیاء": "🛠️",
    }

    message = "🎮 *تقلب بازی اسم و فامیل* 🎮\n\n"

    clean_data = re.sub(r'<.*?>', '', data)
    clean_data = re.sub(r'\s+', ' ', clean_data).strip()

    flag = True
    for key, emoji in sections.items():
        if key in clean_data:
            pattern = rf'{key}\s*[:=]\s*(.*?)(?=\s*(?:[^\s:]+)\s*[:=]|$)'
            match = re.search(pattern, clean_data)
            if match:
                items = match.group(1).strip()
                if items and not items.isdigit() and items.strip() != "":
                    flag = False
                    message += f"{emoji} {key}: \n✅ {items}\n{'—'*20}\n\n"

    if not flag:
        return message
    
def alphabetList():
    alphabet = [
    'الف', 'ب', 'پ', 'ت', 'ث', 'ج', 'چ', 'ح', 'خ', 
    'د', 'ذ', 'ر', 'ز', 'ژ', 'س', 'ش', 'ص', 'ض', 
    'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ک', 'گ', 'ل', 
    'م', 'ن', 'و', 'ه', 'ی']

    markup = InlineKeyboardMarkup()
    i = 2
    for letter in alphabet:
        markup.add(InlineKeyboardButton(text=letter,callback_data=f"esmfamil:{letter}"),row=i//2)
        i += 1
        
    return markup