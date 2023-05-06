from data.workDB import connectToDB

battleMonsters = {}
choiseHero = {}
winProvePlayer = {}
chararactersForChoise = connectToDB("SELECT * FROM Characters")