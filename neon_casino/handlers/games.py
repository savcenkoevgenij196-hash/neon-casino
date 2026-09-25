import random
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from ..games.logic import slots, case
router=Router()

BET=100

def bet_kb(game):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="100 Gold",callback_data=f"bet:{game}:100"),InlineKeyboardButton(text="500 Gold",callback_data=f"bet:{game}:500")],[InlineKeyboardButton(text="1 000 Gold",callback_data=f"bet:{game}:1000"),InlineKeyboardButton(text="Весь баланс",callback_data=f"bet:{game}:all")],[InlineKeyboardButton(text="⬅️ Игры",callback_data="games")]])

@router.callback_query(F.data.in_({"dice","coin","slots","risk","mines","redblack","cases"}))
async def game_open(call:CallbackQuery):
    g=call.data
    if g=="cases": text="📦 КЕЙСЫ\n\nВыбери кейс."
    else: text=f"{ {'dice':'🎲 КУБИК','coin':'🪙 МОНЕТКА','slots':'🎰 СЛОТЫ','risk':'🎯 РИСК','mines':'💣 МИНЫ','redblack':'🎡 КРАСНОЕ / ЧЁРНОЕ'}[g] }\n\nМинимальная ставка: 100 Gold"
    await call.message.edit_text(text,reply_markup=bet_kb(g)); await call.answer()

@router.callback_query(F.data.startswith("bet:"))
async def play(call:CallbackQuery,db):
    _,game,raw=call.data.split(":")
    row=db.get_user(call.from_user.id)
    bet=row['balance'] if raw=='all' else int(raw)
    if bet<100 or bet>row['balance']: return await call.answer("Недостаточно Gold или ставка меньше 100",show_alert=True)
    if game in ('risk','mines','cases'):
        return await call.answer("Этот режим будет подключён в следующем этапе MVP",show_alert=True)
    if db.change_balance(call.from_user.id,-bet,"bet",game) is None: return await call.answer("Баланс изменился, попробуй ещё раз",show_alert=True)
    if game=='dice':
        n=random.randint(1,6); win=n%2==0; mult=1.9; result=f"🎲 Выпало: {n}\n"+('✅ Чётное' if win else '❌ Нечётное')
    elif game=='coin':
        side=random.choice(['Орёл','Решка']); win=side=='Орёл'; mult=1.9; result=f"🪙 Выпало: {side}"
    elif game=='redblack':
        color=random.choice(['🔴 Красное','⚫ Чёрное','🟢 0']); win=color!='🟢 0'; mult=1.9; result=f"🎡 Выпало: {color}"
    else:
        label,mult=slots(); win=mult>0; result=f"🎰 {label}"
    payout=int(bet*mult) if win else 0
    if payout: db.change_balance(call.from_user.id,payout,"win",game)
    db.record_game(call.from_user.id,bet,payout,win,game)
    await call.message.edit_text(f"{result}\n\nСтавка: {bet:,} Gold\n{'🎉 Выигрыш' if win else '💥 Проигрыш'}: {payout:,} Gold".replace(","," "),reply_markup=bet_kb(game)); await call.answer()