import click, hashlib
from socketIO_client import SocketIO

def on_connect_response(*args):
	print 'on_connect_response',args

def on_update_score_reponse(*args):
	print 'on_update_score_reponse', args

def on_get_score_reponse(*args):
	print 'on_get_score_reponse', args

def on_auth_reponse(*args):
	print 'on_auth_reponse', args




@click.group()
def cli():
	"""This Script Reads, arguments should be documented here"""
	pass
	

@cli.command()
def connect():
	with SocketIO('127.0.0.1',5000) as socketIO:
		socketIO.on('connect_response', on_connect_response)
		socketIO.emit('connect')
		socketIO.wait(seconds=1)


@cli.command()
def update_score():
	with SocketIO('127.0.0.1',5000) as socketIO:
		socketIO.on('update_score', on_update_score_reponse)
		socketIO.emit('update_score',{'nickname':'JMaz','game_name':'dojo','score':1099})
		socketIO.wait(seconds=1)



@cli.command()
def get_score():
	with SocketIO('127.0.0.1',5000) as socketIO:
		socketIO.on('get_score', on_get_score_reponse)
		socketIO.emit('get_score',{'nickname':'JMaz','game_name':'dojo'})
		socketIO.wait(seconds=1)

@cli.command()
def get_auth():
	password = hashlib.sha512('fatcat')
	password = password.hexdigest()
        with SocketIO('127.0.0.1',5000) as socketIO:
                socketIO.on('get_auth', on_auth_reponse)
                socketIO.emit('get_auth',{'nickname':'JMaz','password':password})
                socketIO.wait(seconds=1)


