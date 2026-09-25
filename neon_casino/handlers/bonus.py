from datetime import datetime, timezone, timedelta
from aiogram import Router,F
from aiogram.types import CallbackQuery
from ..keyboards.main import main_kb
router=Router()
BONUSES=[1000,1500,2000,3000,5000,7500,15000]
@router.callback_query(F.data=="bonus")
async def bonus(call:CallbackQuery,db):
    r=db.get_user(call.from_user.id); now=datetime.now(timezone.utc)
    if r['last_bonus_at']:
        last=datetime.fromisoformat(r['last_bonus_at'])
        if now-last < timedelta(hours=24):
            left=timedelta(hours=24)-(now-last); h=int(left.total_seconds()//3600); m=int(left.total_seconds()%3600//60)
            return await call.answer(f"Бонус уже получен. Осталось примерно {h}ч {m}м",show_alert=True)
    day=(r['bonus_day']%7)+1; amount=BONUSES[day-1]
    db.change_balance(call.from_user.id,amount,"daily_bonus",f"day={day}")
    with db.connect() as c:c.execute("UPDATE users SET bonus_day=?,last_bonus_at=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",(day,now.isoformat(),call.from_user.id))
    await call.message.edit_text(f"🎁 ДЕНЬ {day}\n\n+{amount:,} Gold\n\nСледующий бонус — через 24 часа.".replace(","," "),reply_markup=main_kb()); await call.answer("Бонус получен!")