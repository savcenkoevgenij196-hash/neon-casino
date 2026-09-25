# 🎰 NEON CASINO

Telegram bot with virtual **Gold** currency. No real-money deposits or withdrawals.

## MVP included
- 10,000 Gold starting balance
- minimum bet 100 Gold, no maximum beyond balance
- Dice, Coin, Slots, Risk, Cases, Mines, Red/Black
- daily 7-day bonus cycle
- profile, statistics, leaderboard
- promo codes
- admin economy/logging foundations
- SQLite persistence
- aiogram 3

## Run
1. Copy `.env.example` to `.env`.
2. Set `BOT_TOKEN` from BotFather.
3. Set `ADMIN_IDS` to comma-separated Telegram numeric IDs.
4. `pip install -r requirements.txt`
5. `python -m neon_casino`

For Render, use a persistent disk for `data/` if you want SQLite data to survive restarts.