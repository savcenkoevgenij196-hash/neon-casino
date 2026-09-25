from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
      [InlineKeyboardButton(text="🎮 Игры", callback_data="games")],
      [InlineKeyboardButton(text="👤 Профиль", callback_data="profile"), InlineKeyboardButton(text="🏆 Топ", callback_data="top")],
      [InlineKeyboardButton(text="🎁 Бонус", callback_data="bonus"), InlineKeyboardButton(text="🎟️ Промокод", callback_data="promo")],
      [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])

def games_kb():
    names=[("🎲 Кубик","dice"),("🪙 Монетка","coin"),("🎰 Слоты","slots"),("🎯 Риск","risk"),("📦 Кейсы","cases"),("💣 Мины","mines"),("🎡 Красное / Чёрное","redblack")]
    rows=[[InlineKeyboardButton(text=n,callback_data=c)] for n,c in names]
    rows.append([InlineKeyboardButton(text="⬅️ Меню",callback_data="menu")])
    return InlineKeyboardMarkup(inline_keyboard=rows)