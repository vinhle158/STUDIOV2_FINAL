import sqlite3
from datetime import datetime
from collections import Counter

db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

now_ms = int(datetime.now().timestamp() * 1000)
thirty_days_ago_ms = now_ms - (30 * 24 * 60 * 60 * 1000)

print('=== USER MESSAGE KEYWORDS (last 30 days) ===')
cur.execute("""
    SELECT substr(json_extract(p.data, '$.text'), 1, 300) as text
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE m.time_created > ?
      AND json_extract(m.data, '$.role') = 'user'
      AND json_extract(p.data, '$.type') = 'text'
      AND length(json_extract(p.data, '$.text')) > 10
    ORDER BY m.time_created DESC
    LIMIT 200
""", (thirty_days_ago_ms,))
rows = cur.fetchall()

# Look for repeated patterns
keywords = ['docker', 'github', 'push', 'deploy', 'git', 'build', 'test', 'api', 'mimo', 'telegram', 'bot', 'server', 'restart', 'check', 'kiểm tra', 'chạy', 'build', 'update', 'cập nhật']
keyword_counts = Counter()
for r in rows:
    text = r['text'].lower() if r['text'] else ''
    for kw in keywords:
        if kw in text:
            keyword_counts[kw] += 1

print('Keyword frequency in user messages:')
for kw, cnt in keyword_counts.most_common(20):
    print(f'  {kw:20s} | {cnt:3d} mentions')

print()
print('=== SESSION TITLES (last 30 days) ===')
cur.execute("""
    SELECT title, directory, time_created
    FROM session
    WHERE time_created > ?
      AND title IS NOT NULL
      AND title NOT LIKE 'checkpoint-writer%'
    ORDER BY time_created DESC
    LIMIT 50
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    tc = datetime.fromtimestamp(r['time_created']/1000).strftime('%m-%d %H:%M')
    d = r['directory'][-30:] if r['directory'] else ''
    print(f'  {tc} | {r["title"][:50]:50s} | {d}')

print()
print('=== BASH COMMANDS WITH DOCKER/GIT (last 30 days) ===')
cur.execute("""
    SELECT substr(json_extract(p.data, '$.state.input'), 1, 200) as cmd
    FROM message m
    JOIN part p ON p.message_id = m.id
    WHERE json_extract(m.data, '$.role') = 'assistant'
      AND json_extract(p.data, '$.type') = 'tool'
      AND json_extract(p.data, '$.tool') = 'bash'
      AND m.time_created > ?
      AND (json_extract(p.data, '$.state.input') LIKE '%docker%' 
           OR json_extract(p.data, '$.state.input') LIKE '%git%'
           OR json_extract(p.data, '$.state.input') LIKE '%npm%')
    ORDER BY m.time_created DESC
    LIMIT 30
""", (thirty_days_ago_ms,))
for r in cur.fetchall():
    print(f'  {r["cmd"][:150]}')

db.close()
