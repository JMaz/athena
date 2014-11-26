import click, hashlib
from socketIO_client import SocketIO


def on_submit_flag_response(*args):
	msg = args[0]
        print(msg['msg'])


def on_get_score_response(*args):
        msg = args[0]
        print(msg['msg'])


def on_get_games_response(*args):
        msg = args[0]
        print(msg['msg'])

def on_get_scoreboard_response(*args):
        msg = args[0]
        print(msg['msg'])



@click.group()
def cli():
	"""This script allows you to interact with the scoreboard
	   you can submit flags, retreive your current score, retreive
	   current scoreboard, and get games you are registered to. You
	   MUST enter your user name and password every time."""
	pass
	


@cli.command()
@click.option('--user',prompt='Enter username')
@click.password_option()
def submit_flag(user,password):
	"""Submit a flag you have found.
	   You will need to provide the
	   game in which the flag is from,
	   the flag name ex KEY00,
	   and the flag value."""
	passwd = hashlib.sha512(password)
	passwd = passwd.hexdigest()
	game_name = click.prompt("Please enter game name")
        flag_name = click.prompt("Please enter flag name! ")
        flag_value = click.prompt("Please enter flag! ")
	if click.confirm("Please verify: "+game_name+"::" + flag_name + "::" +flag_value):
		with SocketIO('127.0.0.1',5000) as socketIO:
                	socketIO.on('submit_flag_response', on_submit_flag_response)
	                socketIO.emit('submit_flag',{'nickname':user,'password':passwd,'game_name':game_name,'flag_name':flag_name,'flag_value':flag_value})
        	        socketIO.wait(seconds=1)



@cli.command()
@click.option('--user',prompt='Enter username')
@click.password_option()
def get_score(user,password):
	"""Get your current score for a specified game. """
        passwd = hashlib.sha512(password)
        passwd = passwd.hexdigest()
        game_name = click.prompt("Please enter game name")
        with SocketIO('127.0.0.1',5000) as socketIO:
		socketIO.on('get_score_response', on_get_score_response)
                socketIO.emit('get_score',{'nickname':user,'password':passwd,'game_name':game_name})
                socketIO.wait(seconds=1)


@cli.command()
@click.option('--user',prompt='Enter username')
@click.password_option()
def get_games(user,password):
	"""Retreive a list of games you are currently registered for."""
        passwd = hashlib.sha512(password)
        passwd = passwd.hexdigest()
        with SocketIO('127.0.0.1',5000) as socketIO:
                socketIO.on('get_games_response', on_get_games_response)
                socketIO.emit('get_games',{'nickname':user,'password':passwd})
                socketIO.wait(seconds=1)

@cli.command()
@click.option('--user',prompt='Enter username')
@click.password_option()
def get_scoreboard(user,password):
	"""Retreive the scoreboard for a specified game you are
	   registered for. """
        passwd = hashlib.sha512(password)
        passwd = passwd.hexdigest()
        game_name = click.prompt("Please enter game name")
        with SocketIO('127.0.0.1',5000) as socketIO:
                socketIO.on('get_scoreboard_response', on_get_scoreboard_response)
                socketIO.emit('get_scoreboard',{'nickname':user,'password':passwd,'game_name':game_name})
                socketIO.wait(seconds=1)
      
