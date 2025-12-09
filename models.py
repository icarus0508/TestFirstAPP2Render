from database import db
from datetime import datetime

# Association Table for Many-to-Many relationship between Member and Event
participation = db.Table('participation',
    db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to events
    events = db.relationship('Event', secondary=participation, back_populates='participants')

    def __repr__(self):
        return f'<Member {self.name}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to members
    participants = db.relationship('Member', secondary=participation, back_populates='events')

    def __repr__(self):
        return f'<Event {self.title}>'
