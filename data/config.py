from aiogram import types, Bot, Dispatcher
Token = "5790692366:AAGwt85uh6eEolaqQJmzWzinvWdCvUXP2uc"
#Token = "1913969492:AAG_tmMbiEcjxUNVDtp0tYn6d8_dtrXshD8"
bot = Bot(token=Token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)