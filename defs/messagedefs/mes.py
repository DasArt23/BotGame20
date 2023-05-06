import aiogram.utils.exceptions
from data.classesRpg import *
from menu.inlineBut import *
from menu.keyboardBut import *
from data.workDB import connectToDB
from data.values import *

floor = '◽️'
wall = '⬛️'
characterEnemy = {3: "🔴", 4: "🟠", 5: "🟡"}
characterPlayer = "🟢"

class Useful:
    def __init__(self, dataMessage):
        self.dataMessage = dataMessage
        self.id = dataMessage.chat.id

    async def SendText(self, text, keyboard=None, val=None, func="answer") -> None:
        """
           Отправка сообщений
           text - текст
           keyboard - клавиатура или название функции
           val - значение функции
           func - тип отправки (answer, edit)
        """
        send = self.dataMessage.answer
        if func == "edit":
            #print('24:', text)
            send = self.dataMessage.edit_text
        if keyboard is None:
            await send(text)
        else:
            try:
                await send(text, reply_markup=keyboard)
                #print(111, text)
            except aiogram.utils.exceptions.BadRequest as er:
                try:
                    await send(text, reply_markup=keyboard())
                    #print(222, text)
                except TypeError:
                    #print(333)
                    await send(text, reply_markup=keyboard(val))

    async def GenerateMonsters(self, Map) -> None:
        battleMonsters[self.id] = {
            3: {},
            4: {},
            5: {},
        }
        for y in range(1, len(Map) - 1):
            for x in range(1, len(Map) - 1):
                monster = Map[y][x]
                if monster == 3:
                    battleMonsters[self.id][monster][f"{x} {y}"] = Monster(hp=2, attack=2, rangeAttack=1, coolDown=1,
                                                                     reward=30)
                elif monster == 4:
                    battleMonsters[self.id][monster][f"{x} {y}"] = Monster(hp=5, attack=1, rangeAttack=2, coolDown=1,
                                                                     reward=20)
                elif monster == 5:
                    battleMonsters[self.id][monster][f"{x} {y}"] = Monster(hp=1, attack=3, rangeAttack=1, coolDown=1,
                                                                     reward=40)

    async def GenerateMap(self, battleMap, hero: Hero):
        returnMap = ""
        for y in range(len(battleMap)):
            for x in range(len(battleMap[y])):
                if battleMap[y][x] == 0:
                    returnMap += floor
                elif battleMap[y][x] == 1:
                    returnMap += wall
                elif battleMap[y][x] == 2:
                    returnMap += characterPlayer
                    hero.y, hero.x = y, x
                elif battleMap[y][x] in (3, 4, 5):
                    returnMap += characterEnemy[battleMap[y][x]]
            returnMap += "\n"
        return returnMap

class Start:
    def __init__(self, dataMessage):
        self.dataMessage = dataMessage
        self.id = dataMessage.chat.id

    async def StartPlay(self):
        choiseHero[self.id] = None
        prove = connectToDB("SELECT Id FROM PlayersCharacters")
        print("Connect is successful")
        if (self.id,) in prove:
            print("Prove")
            await Useful(self.dataMessage).SendText("С возращением", PLayerBase)
        else:
            await Useful(self.dataMessage).SendText(f"Привет {self.dataMessage.chat.first_name}", Menu_start)

    async def ChooseHeroStart(self, call):
        if call.data.split("_")[1] == "Choice":
            if choiseHero[self.id] is None:
                await Useful(dataMessage=self.dataMessage).SendText("Вы никого не выбрали", keyboard=character_choice,
                                                                val=chararactersForChoise, func="edit")
            else:
                print(choiseHero)
                for ch in chararactersForChoise:
                    if choiseHero[self.id] in ch:
                        connectToDB(
                            f"Insert Into PLayersCharacters (Id, Name, Attack, Health, Mana, Agility, Initiative, Callback, AttackRange) Values ({self.id}, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (ch))
                        connectToDB(f"Insert Into RatingPlayers (Id, Rating, Money) Values ({self.id}, {0}, '{0}')")
                        connectToDB(f"UPDATE RatingPlayers SET CountHero = 1 WHERE Id = {self.id}")
                await Useful(dataMessage=self.dataMessage).SendText(
                    f"У вас появиля первый герой - <u>{choiseHero[self.id]}</u>"
                    , func="edit")
                await Useful(dataMessage=self.dataMessage).SendText(
                    "Удачной игры", keyboard=PLayerBase
                )
        else:
            for character in chararactersForChoise:
                if call.data in character:
                    choiseHero[self.id] = character[0]
                    await Useful(dataMessage=self.dataMessage).SendText(
                        f"Вы выбрали: {character[0]}\nАтака: {character[1]}\nЗдоровье: {character[2]}"
                        f"\nМана: {character[3]}\nЛовкость: {character[4]}\nИнициатива: {character[5]}",
                        keyboard=character_choice, val=chararactersForChoise, func="edit")

class Statistic:
    def __init__(self, dataMessage):
        self.dataMessage = dataMessage
        self.id = dataMessage.chat.id

    async def playerStatic(self):
        statsFromDb = connectToDB(f"SELECT * FROM RatingPlayers WHERE Id = {self.id}")[0]
        playerStats = f"Рейтинг: {statsFromDb[1]}\nДеньги: {statsFromDb[2]}\nКоличество героев: {statsFromDb[3]}"
        await Useful(dataMessage=self.dataMessage).SendText(text=playerStats, keyboard=PLayerBase)

    async def heroStatic(self):
        stats = ""
        characters_of_player = connectToDB(f"Select * From PLayersCharacters Where Id = {self.id}")
        for ch in characters_of_player:
            stats += f"{ch[1]}:\nАтака - {ch[2]}\nЗдоровье - {ch[3]}\nМана - {ch[4]}\nЛовкость - {ch[5]}\n" \
                     f"Инициатива - {ch[6]}\nБроня - {ch[11]}"
        await Useful(dataMessage=self.dataMessage).SendText(stats, keyboard=PLayerBase)

    async def menu(self):
        await Useful(dataMessage=self.dataMessage).SendText(text="Выберите тип статистики для просмотра",
                                                            keyboard=Stats)

