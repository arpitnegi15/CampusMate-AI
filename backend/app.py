from flask import Flask, render_template, request, jsonify
from database import init_db, get_answer, get_events_text, get_db, get_timetable_text
import os
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
            static_folder=os.path.join(os.path.dirname(__file__), "..", "static"))

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    lower = msg.lower()

    if "timetable" in lower:
        if "ece" in lower:
            reply = get_timetable_text("ECE")
        elif "mech" in lower or "mechanical" in lower:
            reply = get_timetable_text("MECH")
        else:
            reply = get_timetable_text("CSE")
        return jsonify({"reply": reply})

    if "event" in lower or "hackathon" in lower or "fest" in lower:
        reply = get_events_text()
    else:
        db_ans = get_answer(msg)
        if db_ans:
            reply = db_ans
        elif "hi" in lower or "hello" in lower:
            reply = "Hello! Ask me about Library, Attendance, Fees, HOD, Events or Placement."
        else:
            reply = "Sorry, try Library, Attendance, Fees, HOD, Events or Placement."
    return jsonify({"reply": reply})

@app.route("/admin")
def admin():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM faqs ORDER BY id DESC LIMIT 20")
    faqs = cur.fetchall()
    conn.close()
    return render_template("admin.html", faqs=faqs, events=[])

@app.route("/api/add_faq", methods=["POST"])
def add_faq():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO faqs (keyword, question, answer, category) VALUES (?, ?, ?, ?)",
                (data['keyword'], data['question'], data['answer'], data['category']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/api/add_event", methods=["POST"])
def add_event():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (title, date, time, venue, description) VALUES (?, ?, ?, ?, ?)",
                (data['title'], data['date'], data['time'], data['venue'], data['description']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route("/api/delete_faq/<int:faq_id>", methods=["DELETE"])
def delete_faq(faq_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM faqs WHERE id=?", (faq_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)