from flask import Flask, render_template, request, redirect, session
from models import db, User, Kit, Event, EventRegistration
from urllib.parse import quote_plus
import os
from urllib.parse import quote_plus

app = Flask(__name__)
app.config['SECRET_KEY'] = 'botforge_secure_2026'

# Get password from environment variable
db_password = quote_plus(os.getenv("DB_PASSWORD"))

app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+pymysql://root:{db_password}@localhost/botforge_db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ==========================
# CREATE TABLES
# ==========================

with app.app_context():
    db.create_all()

# ==========================
# LOGIN PAGE
# ==========================

@app.route('/')
def login():
    return render_template('login.html')


# ==========================
# HANDLE LOGIN
# ==========================

@app.route('/login', methods=['POST'])
def handle_login():
    qr_code = request.form['qr_code']
    name = request.form['name']
    email = request.form['email']

    kit = Kit.query.filter_by(qr_code=qr_code).first()

    if not kit:
        return "Invalid QR Code"

    # If kit already activated → login existing user
    if kit.activated:
        existing_user = User.query.filter_by(kit_id=kit.id).first()
        if existing_user:
            session['user_id'] = existing_user.id
            return redirect('/home')
        else:
            return "Error: Kit activated but no user found"

    # First-time activation
    new_user = User(
        name=name,
        email=email,
        kit=kit
    )

    kit.activated = True
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return redirect('/home')


# ==========================
# LOGOUT
# ==========================

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ==========================
# DASHBOARD
# ==========================

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user)


# ==========================
# TUTORIAL SYSTEM
# ==========================

@app.route('/tutorials', methods=['GET', 'POST'])
def tutorials():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        user.tutorial_completed = True
        db.session.commit()
        return redirect('/home')

    return render_template('tutorials.html', user=user)


# ==========================
# TASK SYSTEM
# ==========================

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])

    # Lock tasks until tutorial completed
    if not user.tutorial_completed:
        return redirect('/tutorials')

    if request.method == 'POST':
        time = int(request.form['time'])
        collisions = int(request.form['collisions'])
        energy = int(request.form['energy'])

        score = 100
        score -= time * 0.5
        score -= collisions * 10
        score -= energy * 0.3

        if score < 0:
            score = 0

        user.total_score += int(score)

        # Level unlock logic
        if score >= 70 and user.current_level < 4:
            user.current_level += 1
            user.tutorial_completed = False

        db.session.commit()
        return redirect('/home')

    return render_template('tasks.html', user=user)


# ==========================
# LEADERBOARD
# ==========================

@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.total_score.desc()).all()
    return render_template('leaderboard.html', users=users)


# ==========================
# EVENTS PAGE
# ==========================

@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect('/')

    events = Event.query.all()
    return render_template('events.html', events=events)


# ==========================
# EVENT REGISTRATION
# ==========================

@app.route('/register_event/<int:event_id>')
def register_event(event_id):
    if 'user_id' not in session:
        return redirect('/')

    user_id = session['user_id']

    existing = EventRegistration.query.filter_by(
        user_id=user_id,
        event_id=event_id
    ).first()

    if not existing:
        registration = EventRegistration(
            user_id=user_id,
            event_id=event_id
        )
        db.session.add(registration)
        db.session.commit()

    return redirect('/events')


# ==========================
# RUN APP
# ==========================

if __name__ == '__main__':
    app.run(debug=True)
