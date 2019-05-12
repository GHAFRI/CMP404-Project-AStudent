from config import db

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    email = db.Column(db.String(150))
    points = db.Column(db.String(100))
    course = db.Column(db.String(45))
    user_type = db.Column(db.String(45))
    auth = db.Column(db.String(45))

    def __init__(self, username, password, email, points, course, user_type, auth):
        self.username = username
        self.password = password
        self.email = email
        self.points = points
        self.course = course
        self.user_type = user_type
        self.auth = auth



class notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(45))
    username = db.Column(db.String(45))
    text = db.Column(db.String(254))
    auth = db.Column(db.String(45))


    def __init__(self, course, username, text, auth):
        self.course = course 
        self.username = username
        self.text = text
        self.auth = auth


class discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(45))
    username = db.Column(db.String(45))
    reply_id = db.Column(db.String(45))
    text = db.Column(db.String(254))


    def __init__(self, course, username, text, reply_id):
        self.course = course 
        self.username = username
        self.text = text
        self.reply_id = reply_id







