import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "campusmate.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS faqs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT,
            question TEXT,
            answer TEXT,
            category TEXT
        )
    """)
    cur.execute("SELECT COUNT(*) as c FROM faqs")
    if cur.fetchone()["c"] == 0:
        faqs = [
            ("library", "Library timings?", "Central Library is open Monday to Saturday, 9:00 AM to 6:00 PM.", "Library"),
            ("attendance", "Attendance?", "Minimum 75% attendance is required.", "Attendance"),
            ("fees", "Fees?", "B.Tech Fees Rs. 1,20,000 per year. Accounts Office Room 101.", "Fees"),
            ("cse hod", "HOD CSE?", "Dr. Ramesh Sharma is HOD of CSE. Cabin 204.", "Faculty"),
            ("placement", "Placement?", "85% placed. Highest 12 LPA, Average 4.5 LPA.", "Placement"),
            ("canteen", "Canteen?", "Canteen open 8:30 AM to 6 PM. Thali Rs. 70.", "Canteen"),
            ("bus", "Bus?", "Buses: Gurugram, Dwarka, Palam, Karol Bagh, Noida.", "Transport"),
            ("exam cell", "Exam cell?", "Exam Cell in Admin Block, Room 102.", "Exam"),
            ("timetable", "Timetable?", "Classes 9 AM to 4 PM. Lunch 12:30 to 1:30 PM.", "Timetable"),
            ("library kab", "Library kab khulta hai?", "Library subah 9 baje se shaam 6 baje tak khulta hai.", "Library"),
        ]
        cur.executemany("INSERT INTO faqs (keyword, question, answer, category) VALUES (?, ?, ?, ?)", faqs)
        print("10 FAQs inserted!")
    else:
        print("DB already has data, skipping.")
    conn.commit()
    conn.close()
    print("DB READY!")

def get_answer(msg):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM faqs")
    rows = cur.fetchall()
    conn.close()
    msg = msg.lower()
    best = None
    best_score = 0
    for r in rows:
        score = sum(1 for w in r["keyword"].lower().split() if w in msg)
        if score > best_score:
            best_score = score
            best = r
    if best and best_score > 0:
        return best["answer"]
    return None

def get_events_text():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, time TEXT, venue TEXT, description TEXT)")
    cur.execute("SELECT * FROM events ORDER BY date")
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.executemany("INSERT INTO events (title, date, time, venue, description) VALUES (?, ?, ?, ?, ?)", [
            ("Hackathon 2026 - CodeFest", "2026-11-15", "10:00 AM", "Seminar Hall 2", "24-hour hackathon. Prize Rs. 50,000."),
            ("Tech Talk - AI in 2026", "2026-11-18", "2:00 PM", "Auditorium", "Guest lecture by Google Engineer."),
            ("Cultural Fest - Utsav", "2026-11-22", "11:00 AM", "Main Ground", "Dance, Music, Fashion Show."),
        ])
        conn.commit()
        cur.execute("SELECT * FROM events ORDER BY date")
        rows = cur.fetchall()
    conn.close()
    text = "Upcoming Events:"
    for e in rows:
        text += f"\n- {e['title']} | {e['date']} at {e['time']} | {e['venue']}\n  {e['description']}"
    return text

def get_timetable_text(branch="CSE"):
    timetables = {
        "CSE": "CSE Timetable (Mon-Fri):\n9-10: DBMS | 10-11: OS | 11-12: CN\nLunch 12:30-1:30\n1:30-2:30: AI Lab | 2:30-3:30: Maths",
        "ECE": "ECE Timetable (Mon-Fri):\n9-10: Digital Circuits | 10-11: Signals | 11-12: VLSI\nLunch 12:30-1:30\n1:30-2:30: Embedded Lab | 2:30-3:30: Communication",
        "MECH": "Mechanical Timetable (Mon-Fri):\n9-10: Thermodynamics | 10-11: Fluid Mechanics | 11-12: Machine Design\nLunch 12:30-1:30\n1:30-2:30: Workshop Lab | 2:30-3:30: CAD",
    }
    branch = branch.upper()
    for key in timetables:
        if key in branch:
            return timetables[key]
    return timetables["CSE"]

if __name__ == "__main__":
    init_db()