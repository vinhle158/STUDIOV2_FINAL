import sqlite3
from datetime import datetime, timedelta
from collections import Counter

db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

now_ms = int(datetime.now().timestamp() * 1000)
thirty_days_ago_ms = now_ms - (30 * 24 * 60 * 60 * 1000)

print('=== TOOL USAGE FREQUENCY (last 30 days) ===')
cur.execute("""
    SELECT json_extract(p.data, '$.tool') as tool,
           count(*) as cnt
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND m.time_created > ?
      AND json_extract(p.data, '$.tool') IS NOT NULL
    GROUP BY tool
    ORDER BY cnt DESC
    LIMIT 30
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    print(f'  {r["tool"]:30s} | {r["cnt"]:4d} calls')

print()
print('=== MOST COMMON TOOL INPUTS (last 30 days) ===')
cur.execute("""
    SELECT json_extract(p.data, '$.tool') as tool,
           substr(json_extract(p.data, '$.state.input'), 1, 150) as input_preview,
           count(*) as cnt
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND m.time_created > ?
      AND json_extract(p.data, '$.tool') IS NOT NULL
    GROUP BY tool, input_preview
    HAVING cnt >= 2
    ORDER BY cnt DESC
    LIMIT 50
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    print(f'  {r["cnt"]:3d}x | {r["tool"]:25s} | {r["input_preview"][:80]}')

db.close()
