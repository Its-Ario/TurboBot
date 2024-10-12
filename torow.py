import bale

def torowmenu(*row:list):
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
            t.add(bale.InlineKeyboardButton(x[0],callback_data=x[1]),dx)
        dx += 1
    return t