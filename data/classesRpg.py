
class Hero:
    def __init__(self, id, name, hp, attack, mana, agility, initiative, rangeAttack, arm=None):
        self.id = id
        self.name = name
        self.hp, self.attack = hp, attack
        self.mana, self.agility = mana, agility
        self.initiative = initiative
        self.rangeAttack = rangeAttack
        self.arm = arm

        self.defens = 0
        self.money = 0
        self.x = None
        self.y = None
        self.killMonsters = 0
        self.map = None



    async def minusHp(self, damage=0):
        if self.defens < damage:
            damage -= self.defens
            self.defens = 0
            self.hp -= damage
        else:
            self.defens -= damage
        if self.hp <= 0:
            return True
        return False

    async def end(self):
        self.map = None
        self.killMonsters = 0

    async def moveOnMap(self, direction: [int, int]):
        movingNum = 0
        if direction == [0, 0]:
            return self.map
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if movingNum < 1 and self.map[y][x] == 2:
                    nextElement = self.map[y + direction[0]][x + direction[1]]
                    movingNum += 1
                    if nextElement == 1:
                        break
                    elif nextElement in [3, 4, 5]:
                        break
                    else:
                        self.map[y + direction[0]][x + direction[1]] = 2
                        self.map[y][x] = 0
        return self.map

    async def moveAttack(self, direction: [int, int], monsters):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 2:
                    prove = self.map[y+direction[0]*self.rangeAttack][x+direction[1]*self.rangeAttack] in [3, 4, 5]
                    coordinates = f"{x+direction[1]*self.rangeAttack} {y+direction[0]*self.rangeAttack}"
                    if prove:
                        monsters[self.map[y+direction[0]*self.rangeAttack][x+direction[1]*self.rangeAttack]][coordinates].hp -= self.attack
                        if monsters[self.map[y+direction[0]*self.rangeAttack][x+direction[1]*self.rangeAttack]][coordinates].hp <= 0:
                            self.money += monsters[self.map[y+direction[0]*self.rangeAttack][x+direction[1]*self.rangeAttack]][coordinates].reward
                            self.map[y + direction[0] * self.rangeAttack][x + direction[1] * self.rangeAttack] = 0
                    break
        return self.map

    async def findDamage(self, dictMonsters, endGame) -> None:
        prove = [True, True, True, True]
        damage = 0
        #list_k = []
        for i in range(1, int(len(self.map[0]))):
            #list_k.append(['+coord'])  # add согласно каждой итерации
            directions = [
                [self.x-i, self.y] if prove[0] else [0, 0],
                [self.x+i, self.y] if prove[1] else [0, 0],
                [self.x, self.y-i] if prove[2] else [0, 0],
                [self.x, self.y+i] if prove[3] else [0, 0]
            ]
            damage += await self.findMonsterOrNot(directions, dictMonsters[self.id], prove, i)
        endOrNot = await self.minusHp(damage=damage)
        endGame[self.id] = endOrNot

    async def findMonsterOrNot(self, array, monsters, prove, proveRange):
        damage = 0
        for i in range(0, len(array)):
            try:
                #print(array[i][0], array[i][1], end = ' <-> ')# monsters
                monster = monsters[self.map[array[i][1]][array[i][0]]][f"{array[i][0]} {array[i][1]}"]
                #print([i for i in monsters], "!", monster.rangeAttack)
                if proveRange == monster.rangeAttack:
                    damage += monster.attack
                prove[i] = True
            except KeyError:
                if self.map[array[i][1]][array[i][0]] == 1 and array[i][0] == 0 and array[i][1] == 0:  #условие при котором в этом направлении проверятся не будет сторона
                    prove[i] = False
                else:
                    prove[i] = True
            except IndexError:
                prove[i] = False
        #print("damage: ", damage)
        return damage
        #     positionXY = (0, 0)  # делает шаг вверх
        #     positionXY_new = (0, 1)  # после проверяем всех вокруг игрока
        #     range_list = ['0 +-2', '1 +-2']  # X = -2, -1, 1, 2 and Y=1, X=0 and Y= 3, 2, 0, -1
        # # В итоге сформируется список коррдинат для кроверки там монстров
        # range_list = [(-2, 1), (-1, 1), (1, 1), (2, 1), (0, 3), (0, 2), (0, 0), (0, -1)]
        # for koord in range_list:
        #     pass  # если монстр есть на координате, то проверяем какого он типа, отсюдюда понимает длинну атаки монстра

class Monster:
    def __init__(self, hp: int, attack: int, rangeAttack: int, coolDown: int, reward: int):
        self.hp = hp
        self.attack = attack
        self.rangeAttack = rangeAttack
        self.coolDown = coolDown
        self.reward = reward
        #
        # self.icon = icon

# def visual(column, line) -> str:
#     text = ""
#     c1, c2 = 0, 0
#     for i in line:
#         if i == 2:
#             break
#         c1 += 1
#     for j in column:
#         if j == 2:
#             for k in line:
#                 text += f"{k} "
#             text += f"{j} \n"
#         else:
#             text += f"{' '*(c1*2)}{j}\n"
#     return text

# a1 = Hero(45645753)  # id1
# a2 = Hero(45045753)  # id2
# a3 = Hero(45045793)  # id3
#
# sl = {}
# sl[a1.id] = a1
