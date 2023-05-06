monsters = {
    4:{"typeMonster": "Рядовой",
        "Icons": ["🐊","🐀","🐘","🦝","🦫"],
        0: {
            "name":"Крокодил",
            "hp": 8, 
            "attack": 2,
            "mana": 0,
            "agility": 0,
            "initiative": 1,
            "callback": "monster_Crocodile"
        },
        1: {
            "name":"Крыса",
            "hp": 4, 
            "attack": 4,
            "mana": 0,
            "agility": 20,
            "initiative": 1,
            "callback": "monster_Rat"
        },
        2: {
            "name":"Слон",
            "hp": 10, 
            "attack": 4,
            "mana": 0,
            "agility": 0,
            "initiative": 0,
            "callback": "monster_Elephant"
        },
        3: {
            "name":"Raccoon",
            "hp": 5, 
            "attack": 3,
            "mana": 0,
            "agility": 10,
            "initiative": 3,
            "callback": "monster_Raccoon"
        },
        4: {
            "name":"Beaver",
            "hp": 6, 
            "attack": 4,
            "mana": 0,
            "agility": 5,
            "initiative": 1,
            "callback": "monster_Beaver"
        }
        },
    5:{"typeMonster": "Элитный",
        "Icons": ["🦖","🦕","🦣","🦅"],
        0: {
            "name":"Rex",
            "hp": 12, 
            "attack": 5,
            "mana": 20,
            "agility": 0,
            "initiative": 0,
            "callback": "monster_Rex"
        },
        1: {
            "name":"Динозавр",
            "hp": 16, 
            "attack": 3,
            "mana": 20,
            "agility": 0,
            "initiative": 2,
            "callback": "monster_Dinosaur"
        },
        2: {
            "name":"Мамонт",
            "hp": 20, 
            "attack": 4,
            "mana": 0,
            "agility": 0,
            "initiative": 0,
            "callback": "monster_Mammoth"
        },
        3: {
            "name":"Орел",
            "hp": 7, 
            "attack": 7,
            "mana": 10,
            "agility": 20,
            "initiative": 4,
            "callback": "monster_Eagle"
        }
        },
    6:{"typeMonster": "Босс",
        "Icons": ["🦹‍♂️","🧝‍♂️","🦑","🐉"],
        0: {
            "name":"Здодей",
            "hp": 20, 
            "attack": 8,
            "mana": 80,
            "agility": 20,
            "initiative": 3,
            "callback": "monster_Villain"
        },
        1: {
            "name":"Король Эльфов",
            "hp": 20, 
            "attack": 6,
            "mana": 80,
            "agility": 50,
            "initiative": 4,
            "callback": "monster_KingElf"
        },
        2: {
            "name":"Кракен",
            "hp": 30, 
            "attack": 8,
            "mana": 30,
            "agility": 0,
            "initiative": 0,
            "callback": "monster_Cracen"
        },
        3: {
            "name":"Дракон",
            "hp": 30, 
            "attack": 5,
            "mana": 50,
            "agility": 20,
            "initiative": 1,
            "callback": "monster_Dragon"
        }
        }
    }