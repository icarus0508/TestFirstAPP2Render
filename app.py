import os
from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
from models import Member, Event
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Database configuration
# Use DATABASE_URL from environment if available (for Render), else local sqlite
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    recent_events = Event.query.order_by(Event.date.desc()).limit(5).all()
    member_count = Member.query.count()
    return render_template('index.html', recent_events=recent_events, member_count=member_count)

# --- Member Routes ---
@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        
        if Member.query.filter_by(email=email).first():
            flash('Email already exists!')
        else:
            new_member = Member(name=name, email=email)
            db.session.add(new_member)
            db.session.commit()
            flash('Member added successfully!')
        return redirect(url_for('members'))
    
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)

# --- Event Routes ---
@app.route('/events', methods=['GET', 'POST'])
def events():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        
        try:
            event_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            # Fallback for browsers that might send different format or if user types it
            try:
                event_date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                flash('Invalid date format')
                return redirect(url_for('events'))

        new_event = Event(title=title, description=description, date=event_date)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('events'))

    all_events = Event.query.order_by(Event.date.desc()).all()
    return render_template('events.html', events=all_events)

@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        if member_id:
            member = Member.query.get(member_id)
            if member and member not in event.participants:
                event.participants.append(member)
                db.session.commit()
                flash(f'{member.name} added to event!')
            elif member in event.participants:
                flash('Member already joined this event.')
        return redirect(url_for('event_detail', event_id=event_id))

    # Get members who are NOT in this event for the dropdown
    available_members = [m for m in Member.query.all() if m not in event.participants]
    
    return render_template('event_detail.html', event=event, available_members=available_members)

if __name__ == '__main__':
    app.run(debug=True)
