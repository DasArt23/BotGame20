from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


create_player = KeyboardButton('Создать персонажа')
delete_player = KeyboardButton('Удалить персонажа')
Menu_start = ReplyKeyboardMarkup()
Menu_start.add(create_player, delete_player)


PLayerBase = ReplyKeyboardMarkup()
upgrade = KeyboardButton("Улучшение")
Travel = KeyboardButton("Инвентарь")
stats_but = KeyboardButton("Статистика")
again = KeyboardButton("Начать заново")
shop = KeyboardButton("Магазин")
probFight = KeyboardButton("Бой")
getHero = KeyboardButton("Найм героев")
PLayerBase.add(upgrade, Travel, stats_but, again)
PLayerBase.add(shop, probFight, getHero)

Stats = ReplyKeyboardMarkup()
heroes = KeyboardButton("Статистика героев")
player = KeyboardButton("Статистика игрока")
Stats.add(heroes, player)

Inventory = ReplyKeyboardMarkup()
wareHouse = KeyboardButton("Склад")
weapHouse = KeyboardButton("Оружейная")
Inventory.add(wareHouse, weapHouse)