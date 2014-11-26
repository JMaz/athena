from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, IntegerField, validators
from wtforms.validators import DataRequired, Length
from app.models import User, Game, Flag





class RegisterForm(Form):
        game_name = StringField('game_name',validators=[DataRequired()])
        
        def __init__(self, *args, **kwargs):
                Form.__init__(self, *args, **kwargs)

        def validate(self):
                if not Form.validate(self):
                        return False

                game = Game.query.filter_by(game_name=self.game_name.data).first()

                if game == None:
                        self.game_name.errors.append('This game does not exist. Please choose another one.')
                        return False
                return True



class FlagForm(Form):
        flag_name = StringField('flag_name',validators=[DataRequired()])
	flag_value = StringField('flag_value',validators=[DataRequired()])
	flag_points = IntegerField('flag_points')
	game_name = StringField('game_name',validators=[DataRequired()])
	

        def __init__(self, *args, **kwargs):
                Form.__init__(self, *args, **kwargs)

        def validate(self):
                if not Form.validate(self):
                        return False

                game = Game.query.filter_by(game_name=self.game_name.data).first()

                if game == None:
                        self.game_name.errors.append('This game does not exist. Please choose another one.')
                        return False


		flag = Flag.query.filter_by(game_id=self.game_name.data,flag_name=self.flag_name.data).first()

                if flag != None:
                        self.flag_name.errors.append('This flag name already exist for this game. Please choose another one.')
                        return False

                return True




class GameForm(Form):
	game_name = StringField('game_name',validators=[DataRequired()])
	game_description = TextAreaField('game_description', validators=[Length(min=0, max=140)])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		game = Game.query.filter_by(game_name=self.game_name.data).first()

		if game != None:
			self.game_name.errors.append('This game name is already in use. Please choose another one.')
			return False
		return True

class LoginForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	firstname = StringField('firstname')
	lastname = StringField('lastname')
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

	def validate(self):
		if not Form.validate(self):
			return False

		if self.nickname.data == self.original_nickname:
			return True

		user = User.query.filter_by(nickname=self.nickname.data).first()

		if user != None:
			self.nickname.errors.append('This nickname is already in use. Please choose another one.')
			return False
		
		return True

class SignUpForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password',[validators.DataRequired(), validators.EqualTo('password_check', message='Passwords must match')])
	password_check = PasswordField('password_check', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
                Form.__init__(self, *args, **kwargs)
               
        def validate(self):
                if not Form.validate(self):
                        return False

                user = User.query.filter_by(nickname=self.nickname.data).first()

                if user != None:
                        self.nickname.errors.append('This nickname is already in use. Please choose another one.')
                        return False

		user = User.query.filter_by(email=self.email.data).first()

                if user != None:
                        self.email.errors.append('This email is already in use. Please choose another one.')
                        return False

                return True

