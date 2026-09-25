import asyncio
from aiogram import Bot,Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from .config import get_config
from .db import DB
from .handlers.core import router as core
from .handlers.games import router as games
from .handlers.bonus import router as bonus
from .handlers.admin import router as admin

async def main():
    config=get_config(); db=DB(config.db_path)
    bot=Bot(config.bot_token,default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp=Dispatcher()
    dp.include_router(core);dp.include_router(games);dp.include_router(bonus);dp.include_router(admin)
    # lightweight dependency injection
    dp["db"]=db; dp["config"]=config
    await dp.start_polling(bot,db=db,config=config)

if __name__=='__main__': asyncio.run(main())