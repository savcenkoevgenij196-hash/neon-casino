import sqlite3
from pathlib import Path
from contextlib import contextmanager

SCHEMA = '''
CREATE TABLE IF NOT EXISTS users (
 id INTEGER PRIMARY KEY,
 username TEXT,
 first_name TEXT NOT NULL,
 balance INTEGER NOT NULL DEFAULT 10000,
 games_played INTEGER NOT NULL DEFAULT 0,
 wins INTEGER NOT NULL DEFAULT 0,
 losses INTEGER NOT NULL DEFAULT 0,
 total_wagered INTEGER NOT NULL DEFAULT 0,
 profit INTEGER NOT NULL DEFAULT 0,
 max_win INTEGER NOT NULL DEFAULT 0,
 bonus_day INTEGER NOT NULL DEFAULT 0,
 last_bonus_at TEXT,
 blocked INTEGER NOT NULL DEFAULT 0,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS transactions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER NOT NULL,
 kind TEXT NOT NULL,
 amount INTEGER NOT NULL,
 balance_after INTEGER NOT NULL,
 details TEXT,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS promo_codes (
 code TEXT PRIMARY KEY,
 reward INTEGER NOT NULL,
 max_uses INTEGER,
 uses INTEGER NOT NULL DEFAULT 0,
 expires_at TEXT,
 active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS promo_uses (
 code TEXT NOT NULL,
 user_id INTEGER NOT NULL,
 used_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY(code,user_id),
 FOREIGN KEY(code) REFERENCES promo_codes(code),
 FOREIGN KEY(user_id) REFERENCES users(id)
);
'''

class DB:
    def __init__(self, path: str):
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as con:
            con.executescript(SCHEMA)

    @contextmanager
    def connect(self):
        con = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA journal_mode=WAL")
        try:
            yield con
        finally:
            con.close()

    def ensure_user(self, tg_user):
        with self.connect() as c:
            c.execute("INSERT OR IGNORE INTO users(id,username,first_name) VALUES(?,?,?)", (tg_user.id, tg_user.username, tg_user.first_name or "Игрок"))
            c.execute("UPDATE users SET username=?, first_name=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (tg_user.username, tg_user.first_name or "Игрок", tg_user.id))
            return c.execute("SELECT * FROM users WHERE id=?", (tg_user.id,)).fetchone()

    def get_user(self, uid):
        with self.connect() as c:
            return c.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

    def change_balance(self, uid, delta, kind, details=""):
        with self.connect() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT balance FROM users WHERE id=?", (uid,)).fetchone()
            if not row or row[0] + delta < 0:
                c.execute("ROLLBACK")
                return None
            new = row[0] + delta
            c.execute("UPDATE users SET balance=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (new, uid))
            c.execute("INSERT INTO transactions(user_id,kind,amount,balance_after,details) VALUES(?,?,?,?,?)", (uid,kind,delta,new,details))
            c.execute("COMMIT")
            return new

    def record_game(self, uid, bet, payout, won, details=""):
        with self.connect() as c:
            c.execute("UPDATE users SET games_played=games_played+1, total_wagered=total_wagered+?, wins=wins+?, losses=losses+?, profit=profit+?, max_win=MAX(max_win,?), updated_at=CURRENT_TIMESTAMP WHERE id=?", (bet, int(won), int(not won), payout-bet, max(0,payout), uid))
            bal = c.execute("SELECT balance FROM users WHERE id=?", (uid,)).fetchone()[0]
            c.execute("INSERT INTO transactions(user_id,kind,amount,balance_after,details) VALUES(?,?,?,?,?)", (uid, "game_payout", payout, bal, details))