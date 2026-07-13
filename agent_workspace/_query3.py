import sqlite3
from datetime import datetime
db = sqlite3.connect(r'C:\Users\ROYAL PALACE\.local\share\mimocode\mimocode.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

# Get session IDs for STUDIO V2
cur.execute("SELECT id, title, time_created FROM session WHERE directory LIKE '%STUDIO%' ORDER BY time_created DESC")
sessions = cur.fetchall()
print('=== STUDIO V2 SESSIONS ===')
for s in sessions:
    tc = datetime.fromtimestamp(s['time_created']/1000).strftime('%Y-%m-%d %H:%M')
    print(f'{s["id"]} | {tc} | {s["title"][:60] if s["title"] else "(no title)"}')

# Get recent user messages from STUDIO V2 sessions
print()
print('=== USER MESSAGES IN STUDIO V2 SESSIONS ===')
for s in sessions[:3]:
    cur.execute("""
        SELECT substr(json_extract(p.data, '$.text'), 1, 300) as text
        FROM message m
        JOIN part p ON p.message_id = m.id
        WHERE m.session_id = ?
          AND json_extract(m.data, '$.role') = 'user'
          AND json_extract(p.data, '$.type') = 'text'
        LIMIT 5
    """, (s['id'],))
    rows = cur.fetchall()
    if rows:
        print(f'\nSession: {s["id"][:25]} ({s["title"][:40] if s["title"] else ""})')
        for r in rows:
            t = r['text'][:200] if r['text'] else '(empty)'
            print(f'  > {t}')

db.close()
