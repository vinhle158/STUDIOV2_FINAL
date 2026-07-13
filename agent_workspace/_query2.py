import sqlite3
from datetime import datetime
db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

# Get all session IDs from last 7 days
now_ms = int(datetime.now().timestamp() * 1000)
seven_days_ago_ms = now_ms - (7 * 24 * 60 * 60 * 1000)

print('=== SESSIONS IN LAST 7 DAYS ===')
cur.execute("SELECT id, title, directory, time_created FROM session WHERE time_created > ? ORDER BY time_created DESC", (seven_days_ago_ms,))
sessions = cur.fetchall()
for s in sessions:
    tc = datetime.fromtimestamp(s["time_created"]/1000).strftime('%Y-%m-%d %H:%M')
    print(f'{s["id"]} | {tc} | {s["directory"][-40:]}')

# Get message counts per session
print()
print('=== MESSAGE COUNTS PER SESSION (last 7 days) ===')
for s in sessions:
    cur.execute("SELECT COUNT(*) as cnt FROM message WHERE session_id = ?", (s["id"],))
    cnt = cur.fetchone()["cnt"]
    if cnt > 0:
        print(f'{s["id"][:25]} | {cnt} messages')

# Check for user statements with keywords
print()
print('=== USER STATEMENTS WITH KEYWORDS (last 7 days) ===')
keywords = ['always', 'never', 'remember', 'rule', 'decision', 'decided', 'tradeoff', 'reason', 'repeat', 'again', 'every time', 'workflow', 'luôn', 'không bao giờ', 'quy tắc', 'quyết định']
for kw in keywords:
    cur.execute("""
        SELECT m.session_id, substr(json_extract(p.data, '$.text'), 1, 200) as text
        FROM message m
        JOIN part p ON p.message_id = m.id
        WHERE m.session_id IN (SELECT id FROM session WHERE time_created > ?)
          AND json_extract(m.data, '$.role') = 'user'
          AND json_extract(p.data, '$.type') = 'text'
          AND json_extract(p.data, '$.text') LIKE ?
        LIMIT 5
    """, (seven_days_ago_ms, f'%{kw}%'))
    rows = cur.fetchall()
    if rows:
        print(f'\nKeyword: "{kw}"')
        for r in rows:
            print(f'  {r["session_id"][:20]} | {r["text"][:150]}')

db.close()
