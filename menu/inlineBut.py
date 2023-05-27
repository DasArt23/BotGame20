from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.values import *


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


def createButtonsForChoice(listHeroes):
    buttons = []
    for hero in listHeroes:
        buttons.append(InlineKeyboardButton(text=hero[1], callback_data=f"choiceForBattle_{hero[7]}"))
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Выбрать", callback_data="choiceForBattle_finally_choice"))
    return keyboard


def movingBattle():
    dict_actions = {"Атака": "putbattle_attack", "↑": "putbattle_up"}
    moving = [
        InlineKeyboardButton(text="Атака", callback_data="putbattle_attack"),
        InlineKeyboardButton(text="↑", callback_data="putbattle_up"),
        InlineKeyboardButton(text="Выход", callback_data="putbattle_exit"),
        InlineKeyboardButton(text="←", callback_data="putbattle_left"),
        InlineKeyboardButton(text=" ", callback_data="putbattle_pusto"),
        InlineKeyboardButton(text="→", callback_data="putbattle_right"),
        InlineKeyboardButton(text=" ", callback_data="putbattle_pusto"),
        InlineKeyboardButton(text="↓", callback_data="putbattle_down"),
        InlineKeyboardButton(text=" ", callback_data="putbattle_pusto")
    ]
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(*moving)
    return keyboard


def battleChoseArrow():
    buttons = [
        InlineKeyboardButton(text=" ", callback_data="battle_pusto"),
        InlineKeyboardButton(text="↑", callback_data="battle_up"),
        InlineKeyboardButton(text=" ", callback_data="battle_pusto"),
        InlineKeyboardButton(text="←", callback_data="battle_left"),
        InlineKeyboardButton(text=" ", callback_data="battle_pusto"),
        InlineKeyboardButton(text="→", callback_data="battle_right"),
        InlineKeyboardButton(text=" ", callback_data="battle_pusto"),
        InlineKeyboardButton(text="↓", callback_data="battle_down"),
        InlineKeyboardButton(text=" ", callback_data="battle_pusto")
    ]
    keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard


def shopButtons():
    buttons = [
        InlineKeyboardButton(text="Оружие", callback_data="shop_Weapon"),
        InlineKeyboardButton(text="Броня", callback_data="shop_Armor"),
    ]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def armorShop(armPlayer=None, firstTime=False, call=None):
    armors = allArmors
    print(armors)
    if firstTime:
        armPlayer[call.message.chat.id] = armors
    buttons = [InlineKeyboardButton(text=i[1], callback_data=f"arm_{i[1]}") for i in armors]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Выбрать", callback_data="arm_Choose"))
    return keyboard

def weapHouseOpen(heroes):
    buttons = []
    for hero in heroes:
        buttons.append(InlineKeyboardButton(text=hero[1], callback_data=f"heroChange_{hero[7]}"))
    print(buttons)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Выбрать", callback_data="heroChange_Choose"))
    return keyboard

def changeThings():
    buttons = [
        InlineKeyboardButton(text="Оружие", callback_data=f"heroChange_Weapon"),
        InlineKeyboardButton(text="Броня", callback_data=f"heroChange_Armor")
    ]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

def weapArmChoose(structor):
    buttons = []
    for i in structor:
        if i[3] == 'Arm':
            bafs = connectToDB(f"SELECT HpBaf, DefBaf, Class FROM Armor WHERE ArmorName = '{i[1]}'")[0]
            buttons.append(InlineKeyboardButton(text=i[1], callback_data=f"weapHouseChoose_{i[3]}_{i[1]}.{bafs[0]}.{bafs[1]}.{bafs[2]}"))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Выбрать", callback_data="weapHouseChoose_|_Choose"))
    return keyboard

def chooseClass():
    buttons = [
        InlineKeyboardButton(text="Броня", callback_data="ware_Arm"),
        InlineKeyboardButton(text="Оружие", callback_data="ware_Weap"),
    ]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

def wareChoose(structor):
    buttons = []
    for i in structor:
        if i[3] == 'Arm':
            bafs = connectToDB(f"SELECT HpBaf, DefBaf, Class FROM Armor WHERE ArmorName = '{i[1]}'")[0]
            buttons.append(InlineKeyboardButton(text=i[1], callback_data=f"{i[3]}_{i[1]}.{bafs[0]}.{bafs[1]}.{bafs[2]}"))
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

def chooseHeroToUpg(heroes):
    buttons = [InlineKeyboardButton(text=i[0], callback_data=f"upgradeCh_{i[1]}") for i in heroes]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard

def parametersOfSelectedHero(name, parameters):
    param = [("Атака", 1), ("Здоровье", 1), ("Мана", 10), ("Ловкость", 10), ("Инициатива", 1)]
    original = None
    for ch in chararactersForChoise:
        if ch[0] == name:
            original = (ch[1], ch[2], ch[3], ch[4], ch[5])
            break
    for i in range(len(param)):
        upgradeCoins[param[i][0]] = ((parameters[i]-original[i])/param[i][1])**2*100 if parameters[i] - (original[i]) > 0 else 50
    buttons = [InlineKeyboardButton(text=f"{param[i][0]}<{upgradeCoins[param[i][0]]}>", callback_data=f"parameterHero_{param[i][0]}") for i in range(len(param))]
    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="parameterHero_Назад"))
    return keyboard

def buttonsForHiring():
    pass