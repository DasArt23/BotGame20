from data.config import *
from defs.messagedefs.mes import *

@dp.message_handler(commands='givemoney')
async def giveMoney(message=types.Message):
    connectToDB(f"UPDATE RatingPlayers SET Money = Money + 1000000 WHERE Id = {message.chat.id}")
    await message.answer("Теперь у Вас на 1000000 монет")

