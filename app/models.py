from app import db
from hashlib import md5

class User(db.Model):
	nickname = db.Column(db.String(64), primary_key=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(256),index=True, unique=True)
	firstname  = db.Column(db.String(64),index=True, unique=False)
	lastname  = db.Column(db.String(64),index=True, unique=False)
	scores = db.relationship('Score', backref='player', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.nickname)  # python 2
		except NameError:
			return str(self.nickname)  # python 3

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			version += 1
		return new_nickname


	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Game(db.Model):
	game_name = db.Column(db.String(64), primary_key=True)
	game_description = db.Column(db.String(64), index=True, unique=False)
	instance = db.relationship('Score', backref='game_type', lazy='dynamic')
	flags = db.relationship('Flag', backref='game_type',lazy='dynamic')

	def __repr__(self):
                return '<Game %r>' % (self.game_name)


class Score(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	score = db.Column(db.Integer, default=0)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.String(64), db.ForeignKey('user.nickname'))
	game_id = db.Column(db.String(64), db.ForeignKey('game.game_name'))


	def __repr__(self):
		return '<Score %r>' % (self.score)


class Flag(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	flag_name = db.Column(db.String(15))
	flag_value = db.Column(db.String(256))
	points = db.Column(db.Integer, default=1)
	game_id = db.Column(db.String(64), db.ForeignKey('game.game_name'))
	

	def __repr__(self):
		return'<Flag %r>' % (self.flag_name)
