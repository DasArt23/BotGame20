import types

from data.config import *
from defs.messagedefs.mes import *
from menu.inlineBut import *
from data.values import *
from defs.callbackdefs.call import *
import aiogram

@dp.message_handler(commands='start')
async def procBegin(message: types.Message):
    await Start(dataMessage=message).StartPlay()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Создать персонажа"))
async def CreateHero(message: types.Message):
    choiseHero[message.chat.id] = None
    await Useful(message).SendText("Хорошо, выберите персонажа", keyboard=character_choice, val=chararactersForChoise)

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Начать заново"))
async def againGame(message: types.Message):
    await Useful(message).SendText("Вы уверены?", keyboard=proveAgainGame)

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="again"))
async def proveAgain(call: types.CallbackQuery):
    await Operations(call=call).againProcess()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="character"))
async def chooseHeroStart(call: types.CallbackQuery):
    await Start(dataMessage=call.message).ChooseHeroStart(call=call)

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Статистика"))
async def stats(message: types.Message):
    await Statistic(dataMessage=message).menu()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Статистика игрока"))
async def stats_player(message: types.Message):
    await Statistic(dataMessage=message).playerStatic()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Статистика героев"))
async def stats_heroes(message: types.Message):
    await Statistic(dataMessage=message).heroStatic()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Бой"))
async def battle_start(message: types.Message):
    await Battle(dataMessage=message).startBattle()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Магазин"))
async def getShop(message: types.Message):
    await Shop(dataMessage=message).openShop()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="shop"))
async def section(call: types.CallbackQuery):
    await Shop(call=call).choiceSection()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="arm"))
async def buyArm(call: types.CallbackQuery):
    await Shop(call=call).choiceArm()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Инвентарь"))
async def openWare(message: types.Message):
    await WareHouse(dataMessage=message).openInventory()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Оружейная"))
async def opWeap(message: types.Message):
    await WareHouse(dataMessage=message).openWeapHouse()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="heroChange"))
async def selHero(call: types.CallbackQuery):
    await WareHouse(call=call).changeThing()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="weapHouseChoose"))
async def changeArm(call: types.CallbackQuery):
    await WareHouse(call=call).wearArm()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Склад"))
async def lookAtWare(message: types.Message):
    await WareHouse(dataMessage=message).openWare()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="ware"))
async def WareSection(call: types.CallbackQuery):
    await WareHouse(call=call).WareOpenSect()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="Arm"))
async def WareArmChoose(call: types.CallbackQuery):
    await WareHouse(call=call).ArmChoose()

@dp.message_handler(aiogram.dispatcher.filters.Text(equals="Улучшение"))
async def UpgradeFun(message: types.Message):
    await Upgrade(dataMessage=message).heroUpgrader()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="upgradeCh"))
async def chooseHeroToUpg(call: types.CallbackQuery):
    upgradeHero[call.message.chat.id] = None
    upgradeCoins[call.message.chat.id] = {}
    await Upgrade(call=call).chooseHero(upgradeHero)

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="parameterHero"))
async def chooseHtoUpg(call: types.CallbackQuery):
    print(call.data)
    if call.data.split("_")[1] == "Назад":
        await Upgrade(call=call).heroUpgrader(func="edit")
    else:
        await Upgrade(call=call).chooseParam()

# for i in range(5):
#     print(1)
# else:
#     print("Ok")