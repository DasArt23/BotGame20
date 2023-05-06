import copy
from menu.keyboardBut import *
from data.values import *
from data.workDB import connectToDB
from defs.messagedefs.mes import Useful
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
        winProvePlayer[self.id] = None
        choiseHeroForBattle[self.id] = None
        await self.dataMessage.answer(text="В процессе")

