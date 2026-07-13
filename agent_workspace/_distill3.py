import sqlite3
from datetime import datetime

db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

now_ms = int(datetime.now().timestamp() * 1000)
thirty_days_ago_ms = now_ms - (30 * 24 * 60 * 60 * 1000)

print('=== HIGH-ACTIVITY SESSIONS (last 30 days, >20 messages) ===')
cur.execute("""
    SELECT s.id, s.title, s.directory, s.time_created, COUNT(m.id) as msg_count
    FROM session s
    JOIN message m ON m.session_id = s.id
    WHERE s.time_created > ?
    GROUP BY s.id
    HAVING msg_count > 20
    ORDER BY msg_count DESC
    LIMIT 20
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    tc = datetime.fromtimestamp(r['time_created']/1000).strftime('%m-%d %H:%M')
    d = r['directory'][-35:] if r['directory'] else ''
    t = r['title'][:40] if r['title'] else '(no title)'
    print(f'  {r["msg_count"]:4d} msgs | {tc} | {t:40s} | {d}')

print()
print('=== REPEATED BASH PATTERNS (MiMo API calls) ===')
cur.execute("""
    SELECT substr(json_extract(p.data, '$.state.input'), 1, 250) as cmd, count(*) as cnt
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'bash'
      AND m.time_created > ?
      AND json_extract(p.data, '$.state.input') LIKE '%MIMO_API_KEY%'
    GROUP BY cmd
    ORDER BY cnt DESC
    LIMIT 10
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    print(f'  {r["cnt"]}x | {r["cmd"][:150]}')

print()
print('=== REPEATED BASH PATTERNS (Telegram API calls) ===')
cur.execute("""
    SELECT substr(json_extract(p.data, '$.state.input'), 1, 250) as cmd, count(*) as cnt
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'bash'
      AND m.time_created > ?
      AND json_extract(p.data, '$.state.input') LIKE '%telegram%'
    GROUP BY cmd
    ORDER BY cnt DESC
    LIMIT 10
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    print(f'  {r["cnt"]}x | {r["cmd"][:150]}')

db.close()
