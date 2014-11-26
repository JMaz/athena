import hashlib, datetime
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.socketio import emit
from datetime import datetime
from app import app, db, lm, socketio, salt
from forms import LoginForm, EditForm, SignUpForm, GameForm, RegisterForm, FlagForm
from models import User, Game, Score, Flag



@lm.user_loader
def load_user(id):
	return User.query.get(id)


@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()


@app.route('/')
@app.route('/index')
def index():
	user = g.user
	return render_template("index.html",
				title='Home',
				user=user)


@app.route('/scoreboard')
@login_required
def scoreboard():
	user = g.user

	games = Game.query.all()	
	scores = Score.query.order_by(Score.score.desc()).all()
	
	return render_template("scoreboard.html",
				title='Scoreboard',
				user=user,
				games=games,
				scores=scores)

@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
	form = GameForm()

	user = g.user
	games = Game.query.all()
	


        if form.validate_on_submit():
                game_name = form.game_name.data
                game_description = form.game_description.data
                game = Game(game_name=game_name,game_description=game_description)
                db.session.add(game)
                db.session.commit()
                flash('Your game has been added')
                return redirect(url_for('game'))
        
	return render_template("game.html",
				title='Games',
				user=user,
				games=games,
				form=form)


@app.route('/flag', methods=['GET', 'POST'])
@login_required
def flag():
        form = FlagForm()

        user = g.user
        games = Game.query.all()
	flags = Flag.query.all() 


        if form.validate_on_submit():
                game_name = form.game_name.data
		flag_name = form.flag_name.data
		flag_value = form.flag_value.data
		flag_points = form.flag_points.data

                flag = Flag(game_id=game_name,flag_name=flag_name,flag_value=flag_value,points=flag_points)
                db.session.add(flag)
                db.session.commit()
                flash('Your flag has been added')
                return redirect(url_for('flag'))

        return render_template("flag.html",
                                title='Flag',
                                user=user,
                                games=games,
				flags=flags,
                                form=form)




@app.route('/download')
@login_required
def download():
	user = g.user
	return render_template("download.html",
				title='Downloads')




@app.route('/user/<nickname>')
@login_required
def user(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))

	scores = user.scores.all()

	return render_template('user.html',
				user=user,
				scores=scores)



@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
	form = RegisterForm()

        user = g.user
        games = Game.query.all()
	print(user)
	print(user.nickname)
        if form.validate_on_submit():
                game_type = Game.query.get(form.game_name.data)
		player = User.query.get(user.nickname)
		is_registered = Score.query.filter_by(player=player,game_type=game_type).first()
		if is_registered is None:
	                score = Score(timestamp=datetime.utcnow(),player=player,game_type=game_type)
               		db.session.add(score)
	                db.session.commit()
               		flash('Registration complete')
               		return redirect(url_for('register'))
		else:
			flash('Already registered')
        return render_template("register.html",
                                title='Register',
                                user=user,
                                games=games,
                                form=form)




@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(g.user.nickname)
	
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		g.user.firstname = form.firstname.data
		g.user.lastname = form.lastname.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
		form.firstname.data = g.user.firstname
		form.lastname.data = g.user.lastname
	
	return render_template('edit.html', form=form)


@app.route('/sign_up', methods=['GET','POST'])
def sign_up():
	form = SignUpForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			g.user.nickname = form.nickname.data
			g.user.email = form.email.data
			password = hashlib.sha512(form.password.data)
			g.user.password = password.hexdigest()
			user = User(nickname=g.user.nickname,email=g.user.email,password=g.user.password)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('login'))		
				
	return render_template('sign_up.html',title='Sign Up',form=form)

	

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	
	form = LoginForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			g.user.nickname = form.nickname.data
			password = hashlib.sha512(form.password.data)
			g.user.password = password.hexdigest()
			user = User.query.filter_by(nickname=g.user.nickname,password=g.user.password).first()
			if user is None:
				flash('Username or Password is invalid', 'error')
				return redirect(url_for('login'))
			else:
				login_user(user, remember = form.remember_me.data)
				flash('Logged in successfully')
				return redirect(request.args.get('next') or url_for('index'))	
	return render_template('login.html', 
				title='Sign In',
				form=form)
		

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


#Custom HTTP error handlers
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500




@socketio.on('disconnect')
def test_disconnect():
	emit('response', {'data': 'Disconnected'})
	print('Client disconnected')




@socketio.on('get_scoreboard')
def handle_my_custom_event(json):
        nickname = json['nickname']
        password = json['password']

        user = User.query.filter_by(nickname=nickname,password=password).first()

        if user is None:
                emit('get_scoreboard_response',{'msg':'Invalid username or password'})
        else:

                game_id = json['game_name']
		game = Game.query.get(game_id)

                if game is None:
                        emit('get_scoreboard_response',{'msg':'You are not registered for this game or game does not exist.'})
		else:
               		scoreboard = game.instance.order_by(Score.score.desc()).all()

                	if scoreboard is None:
                        	emit('get_scoreboard_response',{'msg':game_id+ ': No instance of this game is being played.'})
                	else:
				for s in scoreboard:
                        		emit('get_scoreboard_response',{'msg':s.user_id + ' ' + str(s.score)})



@socketio.on('get_games')
def handle_my_custom_event(json):
        nickname = json['nickname']
        password = json['password']

        user = User.query.filter_by(nickname=nickname,password=password).first()

        if user is None:
                emit('get_score_response',{'msg':'Invalid username or password'})
        else:
                score = user.scores.all()
                if score is None:
                        emit('get_games_response',{'msg':'You are not registered for any games.'})
                else:
			for s in score:
	                        emit('get_games_response',{'msg':s.game_id}) 



@socketio.on('get_score')
def handle_my_custom_event(json):
        nickname = json['nickname']
        password = json['password']

        user = User.query.filter_by(nickname=nickname,password=password).first()

        if user is None:
                emit('get_score_response',{'msg':'Invalid username or password'})
        else:

                game_id = json['game_name']

                score = Score.query.filter_by(user_id=nickname,game_id=game_id).first()

                if score is None:
                        emit('get_score_response',{'msg':game_id+ ': You are not registered for this game or game does not exist.'})
                else:
			emit('get_score_response',{'msg':'You have '+str(score.score)+' points in '+game_id})			




@socketio.on('submit_flag')
def handle_my_custom_event(json):
        nickname = json['nickname']
	password = json['password']

	user = User.query.filter_by(nickname=nickname,password=password).first()

        if user is None:
                emit('submit_flag_response',{'msg':'Invalid username or password'})
	else:

		game_id = json['game_name']

		score = Score.query.filter_by(user_id=nickname,game_id=game_id).first()
	
		if score is None:
			emit('submit_flag_response',{'msg':game_id+ ': You are not registered for this game or game does not exist.'})
		else:
			flag_name = json['flag_name']
	
			flag = Flag.query.filter_by(flag_name=flag_name).first()
	
			if flag is None:
				emit('submit_flag_response',{'msg':flag_name+ ':Flag name does not exist -1 to score'})
				s = score.score
				updated = s - 1
				Score.query.filter(Score.user_id==nickname).filter(Score.game_id==game_id).update({'score':updated})
				db.session.commit()

			else:
				flag_value = json['flag_value']
	
				if flag.flag_value == flag_value:
					emit('submit_flag_response',{'msg':flag_name+ ':you gained '+ str(flag.points) +' points'})
					updated = score.score + flag.points
					Score.query.filter(Score.user_id==nickname).filter(Score.game_id==game_id).update({'score':updated})
					db.session.commit()
				
				else:
					emit('submit_flag_response',{'msg':flag_name+ ':you lose '+ str(flag.points) +' points'})
                                        updated = score.score - flag.points
                                        Score.query.filter(Score.user_id==nickname).filter(Score.game_id==game_id).update({'score':updated})
                                        db.session.commit()
		
