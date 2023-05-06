from data.workDB import connectToDB

choiseHeroForBattle = {}
battleMonsters = {}
choiseHero = {}
winProvePlayer = {}
chararactersForChoise = connectToDB("SELECT * FROM Characters")