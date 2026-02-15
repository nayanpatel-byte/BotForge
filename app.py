from flask import Flask, render_template, request, redirect, session
from models import db, User, Kit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'botforge_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

with app.app_context():
    db.create_all()

    if not Kit.query.first():
        sample_kits = [
            Kit(qr_code="KIT12345"),
            Kit(qr_code="KIT67890"),
            Kit(qr_code="KIT11111")
        ]
        db.session.add_all(sample_kits)
        db.session.commit()


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    qr_code = request.form['qr_code']

    kit = Kit.query.filter_by(qr_code=qr_code).first()

    if kit:
        new_user = User(name="Student", qr_code=qr_code)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect('/home')

    return "Invalid or Already Activated QR Code"


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
    return render_template('home.html', user=user)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'user_id' not in session:
        return redirect('/')

    user = User.query.get(session['user_id'])
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

        if score >= 70 and user.current_level < 4:
            user.current_level += 1
            user.tutorial_completed = False  # Reset for next level

        db.session.commit()

        return redirect('/home')

    return render_template('tasks.html', user=user)

    

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



@app.route('/leaderboard')
def leaderboard():
    users = User.query.order_by(User.total_score.desc()).all()
    return render_template('leaderboard.html', users=users)
  
@app.route('/events')
def events():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('events.html')

if __name__ == '__main__':
    app.run(debug=True)
