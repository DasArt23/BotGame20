from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def character_choice(charactersForChoice):
    menu_list = []
    for character in charactersForChoice:
        menu_list.append(InlineKeyboardButton(text=character[0], callback_data=character[6]))
    menu_list.append(InlineKeyboardButton(text="Выбрать", callback_data="character_Choice"))
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*menu_list)
    return keyboard

def proveAgainGame():
    yes_not = [
        InlineKeyboardButton(text="Да", callback_data="again_yes"),
        InlineKeyboardButton(text="Нет", callback_data="again_no")
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*yes_not)
    return keyboard