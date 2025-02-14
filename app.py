from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory storage (Replace with a database later)
conferences = []

class Conference:
    def __init__(self, name, location, date, tickets_available):
        self.name = name
        self.location = location
        self.date = date
        self.tickets_available = tickets_available
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

class Session:
    def __init__(self, title, speaker, time):
        self.title = title
        self.speaker = speaker
        self.time = time

# 🏠 Home Route - Show all conferences
@app.route('/')
def index():
    return render_template('index.html', conferences=conferences)

# ➕ Add Conference (Form + API)
@app.route('/add_conference', methods=['GET', 'POST'])
def add_conference():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        date = request.form['date']
        tickets_available = 'tickets_available' in request.form
        conference = Conference(name, location, date, tickets_available)
        conferences.append(conference)
        return redirect(url_for('index'))
    return render_template('add_conference.html')

# ➕ Add Session (Form + API)
@app.route('/add_session/<conference_name>', methods=['GET', 'POST'])
def add_session(conference_name):
    conference = next((conf for conf in conferences if conf.name == conference_name), None)
    if conference is None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        speaker = request.form['speaker']
        time = request.form['time']
        session = Session(title, speaker, time)
        conference.add_session(session)
        return redirect(url_for('index'))
    
    return render_template('add_session.html', conference=conference)

# 📌 API Route to get all conferences (JSON)
@app.route('/api/conferences', methods=['GET'])
def get_conferences():
    return jsonify([
        {
            "name": conf.name,
            "location": conf.location,
            "date": conf.date,
            "tickets_available": conf.tickets_available,
            "sessions": [{"title": s.title, "speaker": s.speaker, "time": s.time} for s in conf.sessions]
        } for conf in conferences
    ])

# 🚀 Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
