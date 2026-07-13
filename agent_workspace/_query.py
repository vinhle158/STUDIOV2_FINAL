import sqlite3
from datetime import datetime, timedelta
db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

# time_created is in milliseconds epoch
now_ms = int(datetime.now().timestamp() * 1000)
seven_days_ago_ms = now_ms - (7 * 24 * 60 * 60 * 1000)

print('=== RECENT SESSIONS FOR STUDIO V2 (last 7 days) ===')
cur.execute("SELECT id, title, directory, time_created, time_updated FROM session WHERE directory LIKE '%STUDIO%' AND time_created > ? ORDER BY time_created DESC LIMIT 20", (seven_days_ago_ms,))
rows = cur.fetchall()
for r in rows:
    tc = datetime.fromtimestamp(r["time_created"]/1000).strftime('%Y-%m-%d %H:%M')
    t = r["title"][:70] if r["title"] else "(no title)"
    print(f'{r["id"][:25]} | {t} | {tc}')

print()
print('=== ALL STUDIO V2 SESSIONS ===')
cur.execute("SELECT id, title, time_created FROM session WHERE directory LIKE '%STUDIO%' ORDER BY time_created DESC LIMIT 20")
rows = cur.fetchall()
for r in rows:
    tc = datetime.fromtimestamp(r["time_created"]/1000).strftime('%Y-%m-%d %H:%M')
    t = r["title"][:70] if r["title"] else "(no title)"
    print(f'{r["id"][:25]} | {t} | {tc}')

print()
print('=== ALL RECENT SESSIONS (last 7 days, all dirs) ===')
cur.execute("SELECT id, title, directory, time_created FROM session WHERE time_created > ? ORDER BY time_created DESC LIMIT 20", (seven_days_ago_ms,))
rows = cur.fetchall()
if not rows:
    print('(none found)')
for r in rows:
    tc = datetime.fromtimestamp(r["time_created"]/1000).strftime('%Y-%m-%d %H:%M')
    t = r["title"][:50] if r["title"] else "(no title)"
    d = r["directory"][-40:] if r["directory"] else ""
    print(f'{r["id"][:25]} | {t} | {tc} | {d}')

db.close()
