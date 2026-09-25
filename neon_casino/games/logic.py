import random

DICE = [("more3", lambda x:x>3, 1.9), ("less4", lambda x:x<4, 1.9), ("even", lambda x:x%2==0, 1.9), ("odd", lambda x:x%2==1, 1.9)]
SLOTS = [
 ("❌ No combo", .55, 0), ("🍒🍒🍒", .20, 2), ("🍋🍋🍋", .12, 3), ("🔔🔔🔔", .07, 5),
 ("💎💎💎", .04, 10), ("7️⃣7️⃣7️⃣", .015, 25), ("👾👾👾", .0045, 50), ("🌌 NEON JACKPOT", .0005, 250)]
CASES = {
 "normal": (1000, [(0,.10),(250,.20),(500,.25),(1000,.25),(2000,.15),(5000,.045),(10000,.005)]),
 "rare": (5000, [(500,.10),(1000,.15),(2500,.20),(5000,.25),(10000,.17),(25000,.10),(50000,.03)]),
 "elite": (25000, [(2500,.10),(5000,.15),(10000,.20),(25000,.25),(50000,.17),(100000,.10),(250000,.03)]),
 "neon": (100000, [(10000,.15),(25000,.20),(50000,.25),(100000,.20),(250000,.12),(500000,.07),(1000000,.01)])}

def weighted(items):
    r=random.random(); acc=0
    for value,p in items:
        acc += p
        if r <= acc: return value
    return items[-1][0]

def slots():
    r=random.random(); acc=0
    for label,p,m in SLOTS:
        acc += p
        if r <= acc: return label,m
    label,p,m=SLOTS[-1]; return label,m

def case(kind):
    price, items=CASES[kind]; return price, weighted(items)