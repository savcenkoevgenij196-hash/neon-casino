from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from ..keyboards.main import main_kb, games_kb

router=Router()

def menu_text(row):
    return f"🎰 NEON CASINO\n\n💰 Баланс: {row['balance']:,} Gold\n\nВыбирай игру или раздел ниже.".replace(","," ")

@router.message(CommandStart())
async def start(message: Message, db):
    row=db.ensure_user(message.from_user)
    if row['blocked']:
        return await message.answer("⛔ Доступ заблокирован.")
    await message.answer(menu_text(row), reply_markup=main_kb())

@router.callback_query(F.data=="menu")
async def menu(call: CallbackQuery, db):
    row=db.ensure_user(call.from_user); await call.message.edit_text(menu_text(row), reply_markup=main_kb()); await call.answer()

@router.callback_query(F.data=="games")
async def games(call: CallbackQuery):
    await call.message.edit_text("🎮 ИГРЫ\n\nМинимальная ставка: 100 Gold\nМаксимум: весь твой баланс.", reply_markup=games_kb()); await call.answer()

@router.callback_query(F.data=="profile")
async def profile(call: CallbackQuery, db):
    r=db.get_user(call.from_user.id)
    text=f"👤 ПРОФИЛЬ\n\nID: {r['id']}\n💰 Баланс: {r['balance']:,} Gold\n🎮 Игр: {r['games_played']}\n✅ Побед: {r['wins']}\n❌ Поражений: {r['losses']}\n💸 Оборот: {r['total_wagered']:,} Gold\n📈 Профит: {r['profit']:,} Gold\n🏆 Макс. выигрыш: {r['max_win']:,} Gold".replace(","," ")
    await call.message.edit_text(text,reply_markup=main_kb()); await call.answer()

@router.callback_query(F.data=="top")
async def top(call: CallbackQuery, db):
    with db.connect() as c: rows=c.execute("SELECT username,first_name,balance FROM users WHERE blocked=0 ORDER BY balance DESC LIMIT 10").fetchall()
    text="🏆 NEON TOP\n\n"+"\n".join(f"{i}. @{r['username']} — {r['balance']:,} Gold" if r['username'] else f"{i}. {r['first_name']} — {r['balance']:,} Gold" for i,r in enumerate(rows,1)).replace(","," ")
    await call.message.edit_text(text or "Пока пусто.",reply_markup=main_kb()); await call.answer()

@router.callback_query(F.data=="help")
async def help_(call: CallbackQuery):
    await call.message.edit_text("ℹ️ Помощь\n\nВсе Gold виртуальные. Минимальная ставка — 100 Gold. Нельзя поставить больше текущего баланса.\n\nИгры: 🎲 🪙 🎰 🎯 📦 💣 🎡",reply_markup=main_kb()); await call.answer()