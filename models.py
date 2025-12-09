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
    profile_image = db.Column(db.String(255)) # Path to uploaded image

    def __repr__(self):
        return f'<Member {self.name}>'

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional: Link to uploader (Member)
    # uploader_id = db.Column(db.Integer, db.ForeignKey('member.id'))

    def __repr__(self):
        return f'<Photo {self.filename}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to members
    participants = db.relationship('Member', secondary=participation, back_populates='events')
    # Relationship to photos
    photos = db.relationship('Photo', backref='event', lazy=True)

    def __repr__(self):
        return f'<Event {self.title}>'
