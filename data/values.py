from data.workDB import connectToDB

choiseHeroForBattle = {}
battleMonsters = {}
choiseHero = {}
winProvePlayer = {}
chararactersForChoise = connectToDB("SELECT * FROM Characters")
allArmors = connectToDB("SELECT * FROM Armor")
endOfGame = {}
armorsForPlayer, armorsForPlayerChoose = {}, {}
thingWear, thingsMove = {}, {}
upgradeHero, upgradeCoins = {}, {}