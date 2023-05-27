from data.config import *
from menu.inlineBut import *
from data.values import *
from defs.callbackdefs.call import *
import aiogram

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="choiceForBattle"))
async def choiceForEpicBattle(call: types.CallbackQuery):
    await Battle(call=call).choiceHero()

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="putbattle"))
async def moveOnMap(call: types.CallbackQuery):
    direction = call.data.split("_")[1]
    keyboard = movingBattle()
    prove, mapBat, text = False, "", ""
    if direction == "attack":
        mapBat = await Useful(dataMessage=call.message)\
            .GenerateMap(choiseHeroForBattle[call.message.chat.id].map, choiseHeroForBattle[call.message.chat.id])
        keyboard = battleChoseArrow()
    elif direction == "exit":
        mapBat, prove = "", True
    else:
        mapBat = await Battle(call=call).moving(choiseHeroForBattle[call.message.chat.id])
    await choiseHeroForBattle[call.message.chat.id].findDamage(battleMonsters, endGame=endOfGame)
    text += await Useful(dataMessage=call.message).retHeroBattleStatistic(choiseHeroForBattle[call.message.chat.id])
    text += mapBat
    await Useful(dataMessage=call.message).SendText(text, func="edit", keyboard=keyboard)
    if endOfGame[call.message.chat.id] or prove:
        connectToDB(f"UPDATE RatingPlayers SET Money = Money + {choiseHeroForBattle[call.message.chat.id].money} WHERE Id = {call.message.chat.id}")
        await Useful(dataMessage=call.message).SendText(text=f"Игра окончена\nДенег: {choiseHeroForBattle[call.message.chat.id].money}", func="edit")
        await choiseHeroForBattle[call.message.chat.id].end()
        choiseHeroForBattle[call.message.chat.id] = None

@dp.callback_query_handler(aiogram.dispatcher.filters.Text(startswith="battle"))
async def attack(call: types.CallbackQuery):
    await Battle(call=call).attackMove()