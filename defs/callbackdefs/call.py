import copy
from menu.keyboardBut import *
from data.values import *
from data.workDB import connectToDB
from defs.messagedefs.mes import Useful
from menu.inlineBut import *
from data.classesRpg import *
from data.maps import *


class Operations:
    def __init__(self, call):
        self.call = call
        self.id = call.message.chat.id

    async def againProcess(self):
        if self.call.data.split("_")[1] == "yes":
            connectToDB(f"DELETE From PLayersCharacters WHERE Id = {self.call.message.chat.id}")
            connectToDB(f"DELETE From RatingPlayers WHERE Id = {self.call.message.chat.id}")
            connectToDB(f"DELETE FROM Warehouse WHERE Id = {self.call.message.chat.id}")
            prove = connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.call.message.chat.id}")
            print(68, prove)
            await Useful(dataMessage=self.call.message).SendText("Для того чтобы начать напишите /start", func="edit")
        else:
            await Useful(dataMessage=self.call.message).SendText("Ok", func="edit")


class Battle:
    def __init__(self, dataMessage=None, call=None):
        self.call = call
        self.dataMessage = dataMessage if call is None else call.message
        self.id = call.message.chat.id if dataMessage is None else dataMessage.chat.id

    async def startBattle(self):
        winProvePlayer[self.id] = False
        choiseHeroForBattle[self.id] = None
        playersCharacters = connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.id}")
        print(playersCharacters)
        await Useful(dataMessage=self.dataMessage).SendText(text="Выберите героя",
                                                            keyboard=createButtonsForChoice(playersCharacters))

    async def choiceHero(self):
        playersCharacters = connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.id}")
        keyboard = createButtonsForChoice(playersCharacters)
        prove = self.call.data.split("_")[2]
        if prove == "choice":
            if choiseHeroForBattle[self.id] is None:
                text = "Выберите героя"
            else:
                text = f"Вы выбрали {choiseHeroForBattle[self.id].name}\n"
                if not (choiseHeroForBattle[self.id].arm is None):
                    choiseHeroForBattle[self.id].hp += \
                        connectToDB(f"SELECT HpBaf FROM Armor WHERE ArmorName = '{choiseHeroForBattle[self.id].arm}'")[
                            0][0]
                    choiseHeroForBattle[self.id].defens += \
                        connectToDB(f"SELECT DefBaf FROM Armor WHERE ArmorName = '{choiseHeroForBattle[self.id].arm}'")[
                            0][
                            0]
                choiseHeroForBattle[self.id].map = copy.deepcopy(MapForBattle)
                text += await Useful(dataMessage=self.dataMessage).retHeroBattleStatistic(choiseHeroForBattle[self.id])
                text += await Useful(dataMessage=self.dataMessage).GenerateMap(choiseHeroForBattle[self.id].map,
                                                                               choiseHeroForBattle[self.id])
                await Useful(dataMessage=self.dataMessage).GenerateMonsters(choiseHeroForBattle[self.id].map)
                print(battleMonsters)
                keyboard = movingBattle()
                endOfGame[self.id] = False
        else:
            characters = {
                "Archer": "Лучник",
                "Warrior": "Воин"
            }
            character = connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.id} "
                                    f"AND Name = '{characters[prove]}'")[0]
            print(character)
            choiseHeroForBattle[self.id] = Hero(
                id=self.id,
                name=character[1],
                hp=character[3],
                attack=character[2],
                mana=character[4],
                agility=character[5],
                initiative=character[6],
                rangeAttack=character[8],
                arm=character[11],
            )
            text = f"Вы выбрали {choiseHeroForBattle[self.id].name}а"
        await Useful(dataMessage=self.dataMessage).SendText(text=text, keyboard=keyboard, func="edit")

    async def moving(self, player: Hero):
        if self.call.data.split("_")[1] in ("attack", "pusto"):
            return
        directions = {
            "left": [0, -1], "up": [-1, 0], "right": [0, 1], "down": [1, 0]
        }
        direction = directions[self.call.data.split("_")[1]]
        mapPlayer = await Useful(dataMessage=self.dataMessage).GenerateMap(await player.moveOnMap(direction=direction),
                                                                           hero=player)
        return mapPlayer

    async def attackMove(self):
        direction = self.call.data.split("_")[1]
        if direction == "pusto":
            await Useful(dataMessage=self.call.message).SendText("Выберите направление")
            return None
        directions = {
            "left": [0, -1],
            "up": [-1, 0],
            "right": [0, 1],
            "down": [1, 0],
        }
        await choiseHeroForBattle[self.id].moveAttack(directions[direction], battleMonsters[self.id]),
        text = await Useful(dataMessage=self.call.message).retHeroBattleStatistic(choiseHeroForBattle[self.id])
        text += await Useful(dataMessage=self.call.message).GenerateMap(choiseHeroForBattle[self.id].map,
                                                                        choiseHeroForBattle[self.id])
        await Useful(dataMessage=self.call.message).SendText(text=text, keyboard=movingBattle(), func="edit")


class Shop:
    def __init__(self, dataMessage=None, call=None):
        self.call = call
        self.dataMessage = call.message if dataMessage is None else dataMessage
        self.id = self.dataMessage.chat.id

    async def openShop(self):
        await Useful(dataMessage=self.dataMessage).SendText("Выберите раздел", keyboard=shopButtons())

    async def choiceSection(self):
        sectionType = self.call.data.split("_")[1]
        if sectionType == "Weapon":
            pass
        elif sectionType == "Armor":
            armorsForPlayer[self.call.message.chat.id] = None
            await Useful(dataMessage=self.call.message).SendText("Выберите броню",
                                                                 func="edit",
                                                                 keyboard=armorShop(
                                                                     armPlayer=armorsForPlayer,
                                                                     firstTime=True,
                                                                     call=self.call,
                                                                 ))

    async def choiceArm(self):
        """Выбор брони и ее покупка"""
        nameArmor = self.call.data.split("_")[1]
        if nameArmor == "Choose":
            if armorsForPlayerChoose[self.id] is None:
                await Useful(dataMessage=self.dataMessage).SendText("Выберите броню")
            else:
                playerMoney = connectToDB(f"SELECT Money FROM RatingPlayers WHERE Id = {self.id}")[0][0]
                if playerMoney < armorsForPlayerChoose[self.id][5]:
                    await Useful(dataMessage=self.dataMessage).SendText("Не хватает денег")
                else:
                    playerMoney -= armorsForPlayerChoose[self.id][5]
                    connectToDB(f"UPDATE RatingPlayers SET Money = {playerMoney} WHERE Id = {self.id}")
                    if not connectToDB(
                            f"SELECT ThingName FROM Warehouse WHERE Id = {self.id} AND ThingName = '{armorsForPlayerChoose[self.id][1]}'"):
                        connectToDB(
                            f"INSERT INTO Warehouse (Id, ThingName, Amount, Class) VALUES ({self.id}, '{armorsForPlayerChoose[self.id][1]}', 1, 'Arm')")
                    else:
                        connectToDB(
                            f"UPDATE Warehouse SET Amount = Amount + 1 WHERE ThingName = '{armorsForPlayerChoose[self.id][1]}' AND Id = {self.id}")
                    await Useful(dataMessage=self.dataMessage).SendText(
                        f"У вас появился новый предмет: {armorsForPlayerChoose[self.id][1]} броня")
        else:
            for i in armorsForPlayer[self.id]:
                print(i, 111)
                if nameArmor in i:
                    await Useful(dataMessage=self.dataMessage).SendText(
                        f"Название: {i[1]}\nПрибавка❤️: {i[2]}\nПрибавка🛡"
                        f": {i[3]}\nЦена: {i[5]}", keyboard=armorShop(), func="edit")
                    armorsForPlayerChoose[self.id] = i
                    break


class WareHouse:
    def __init__(self, dataMessage=None, call=None):
        self.call = call
        self.dataMessage = call.message if dataMessage is None else dataMessage
        self.id = self.dataMessage.chat.id

    async def openInventory(self):
        await Useful(dataMessage=self.dataMessage).SendText(
            "Выберите куда вам надо", keyboard=Inventory
        )

    async def openWeapHouse(self):
        heroes = connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.id}")
        choiseHero[self.id] = None
        print(heroes, '&^%')
        await Useful(dataMessage=self.dataMessage).SendText("Вы вошли в оружейную",
                                                            keyboard=PLayerBase)
        await Useful(dataMessage=self.dataMessage).SendText("Выберите героя",
                                                            keyboard=weapHouseOpen,
                                                            val=heroes)

    async def changeThing(self):
        dataBase = self.call.data.split("_")
        if dataBase[1] == "Choose":
            if choiseHero[self.id] is None:
                await Useful(dataMessage=self.dataMessage).SendText("Вы не выбрали героя")
            else:
                await Useful(dataMessage=self.dataMessage).SendText(f"Вы выбрали {choiseHero[self.id][1]}",
                                                                    keyboard=changeThings(), func="edit")
        if dataBase[1] == "character":
            choiseHero[self.id] = connectToDB(
                f"SELECT * FROM PLayersCharacters WHERE Callback = '{dataBase[1]}_{dataBase[2]}' AND Id = {self.id}")[
                0]
            hero = choiseHero[self.id]
            await Useful(dataMessage=self.dataMessage).SendText(
                f"{hero[1]}\nАтака: {hero[2]}\nЗдоровье: {hero[3]}\nМана: {hero[4]}\nЛовксть: {hero[5]}\nИнициатива: {hero[6]}\n"
                f"Дистанция атаки: {hero[8]}\n"
                f"Оружие: {'Нет' if hero[9] is None else hero[9]}, {'Нет' if hero[10] is None else hero[10]}\nБроня: {'Нет' if hero[11] is None else hero[11]}",
                keyboard=weapHouseOpen(
                    connectToDB(f"SELECT * FROM PLayersCharacters WHERE Id = {self.id}")), func="edit")
        if dataBase[1] == "Weapon":
            pass
        if dataBase[1] == "Armor":
            armors = connectToDB(f"SELECT * FROM Warehouse WHERE Id = {self.id} AND Class = 'Arm'")
            await Useful(dataMessage=self.dataMessage).SendText(f"Выберите броня для {choiseHero[self.id][1]}",
                                                                keyboard=weapArmChoose(armors), func="edit")

    async def wearArm(self):
        thingData = self.call.data.split("_")[2]
        species = thingData.split(".")
        if species[0] == "Choose":
            if thingWear[self.id] is None:
                await Useful(dataMessage=self.dataMessage).SendText("Вы не выбрали вещь")
            else:
                if connectToDB(f"SELECT Amount FROM Warehouse WHERE Id = {self.id} AND ThingName = '{thingWear[self.id][0]}'")[0][0] == 0:
                    await Useful(dataMessage=self.dataMessage).SendText("На складе таких вещей нет")
                else:
                    connectToDB(f"UPDATE PlayersCharacters SET ArmorId = '{thingWear[self.id][0]}' WHERE Id = {self.id} AND Name = '{choiseHero[self.id][1]}'")
                    connectToDB(f"UPDATE Warehouse SET Amount = Amount - 1 WHERE ThingName = '{thingWear[self.id][0]}' AND Id = {self.id}")
                    await Useful(dataMessage=self.dataMessage).SendText(f"Теперь у {choiseHero[self.id][1]}а броня {thingWear[self.id][0]}")
        else:
            thingData = thingData.split(".")
            thingWear[self.id] = thingData
            await Useful(dataMessage=self.dataMessage).SendText(f"Вы выбрали {thingWear[self.id][0]}")

    async def openWare(self):
        plaWareH = connectToDB(f"SELECT * FROM Warehouse WHERE Id = {self.id}")
        await Useful(dataMessage=self.dataMessage).SendText("Вы вошли на склад", keyboard=PLayerBase)
        if not plaWareH:
            await Useful(dataMessage=self.dataMessage).SendText("На вашем складе пока ничего нет")
        else:
            thingWear[self.id] = None
            await Useful(dataMessage=self.dataMessage).SendText("Выберите класс", keyboard=chooseClass())

    async def WareOpenSect(self):
        typeThing = self.call.data.split("_")[1]
        things = connectToDB(f"SELECT * FROM Warehouse WHERE Id = {self.id} AND Class = '{typeThing}'")
        thingsMove[self.id] = things
        if not things:
            await Useful(dataMessage=self.dataMessage).SendText("У вас нет снаряжение такого типа")
        else:
            await Useful(dataMessage=self.dataMessage).SendText("Выберите снаряжение", keyboard=wareChoose(things),
                                                                func="edit")

    async def ArmChoose(self):
        nameArm = self.call.data.split("_")[1]
        stats = nameArm.split(".")
        amount = connectToDB(
            f"SELECT Amount FROM Warehouse WHERE Id = {self.id} AND ThingName = '{stats[0]}'")
        await Useful(dataMessage=self.dataMessage).SendText(f"{stats[0]}\nПрибавка ❤️: {stats[1]}\nПрибавка 🛡: {stats[2]}\nКласс: {stats[3]}\nКоличество: {amount[0][0]}",
                                                            keyboard=wareChoose(thingsMove[self.id]), func="edit")
class Upgrade:
    def __init__(self, dataMessage=None, call=None):
        self.call = call
        self.dataMessage = call.message if dataMessage is None else dataMessage
        self.id = self.dataMessage.chat.id

    async def heroUpgrader(self, func="answer"):
         playerCharacters = connectToDB(f"SELECT Name, Callback FROM PLayersCharacters WHERE Id = {self.id}")
         await Useful(dataMessage=self.dataMessage).SendText(
             "Выберите героя", keyboard=chooseHeroToUpg(playerCharacters), func=func
         )

    async def chooseHero(self, hero):
        selectedHeroParameters = connectToDB(f"SELECT Attack, Health, Mana, Agility, Initiative, AttackRange FROM PLayersCharacters WHERE Id = {self.id} "
                                             f"AND Callback = '{self.call.data.split('_')[1] + '_' + self.call.data.split('_')[2]}'")[0]
        print(selectedHeroParameters)
        name = connectToDB(f"SELECT Name FROM PLayersCharacters WHERE Id = {self.id} AND Callback = '{self.call.data.split('_')[1] + '_' + self.call.data.split('_')[2]}'")[0][0]
        hero[self.id] = Hero(
            id=self.id,
            name=name,
            hp=selectedHeroParameters[1],
            attack=selectedHeroParameters[0],
            mana=selectedHeroParameters[2],
            agility=selectedHeroParameters[3],
            initiative=selectedHeroParameters[4],
            rangeAttack=selectedHeroParameters[5],
        )
        await Useful(dataMessage=self.dataMessage).SendText(await Useful(dataMessage=self.dataMessage).retHeroBattleStatistic(hero[self.id]),
                                                            keyboard=parametersOfSelectedHero(name, selectedHeroParameters), func="edit")
    async def chooseParam(self):
        parametrsChangeName = {
            "Атака": ("Attack", 1),
            "Здоровье": ("Health", 1),
            "Мана": ("Mana", 10),
            "Ловкость": ("Agility", 10),
            "Инициатива": ("Initiative", 1),
        }
        param = parametrsChangeName[self.call.data.split("_")[1]][0]
        playerMoney = connectToDB(f"SELECT Money FROM RatingPlayers WHERE Id = {self.id}")[0][0]
        if playerMoney < upgradeCoins[self.call.data.split("_")[1]]:
            await Useful(dataMessage=self.dataMessage).SendText("Не хватает монет")
        else:
            connectToDB(f"UPDATE RatingPlayers SET Money = {playerMoney - upgradeCoins[self.call.data.split('_')[1]]}")
            connectToDB(f"UPDATE PLayersCharacters SET {param} = {param} + {parametrsChangeName[self.call.data.split('_')[1]][1]}")
            await self.heroUpgrader(func="edit")