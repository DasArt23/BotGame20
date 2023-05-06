
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
    await Battle(dataMessage=message).startBattle(choiseHero)