from socketIO_client import SocketIO

def on_connect_response(*args):
	print 'on_connect_response',args


with SocketIO('127.0.0.1',5000) as socketIO:
	socketIO.on('connect_response', on_connect_response)
	socketIO.emit('connect')
	socketIO.wait(seconds=1)
#	socketIO.emit('update_score',{'nickname':'JMaz','game_name':'intruder','score':-100})
#	socketIO.wait(seconds=1)
#	socketIO.on('score_updated',score_updated)
#	socketIO.wait(seconds=1)
#	socketIO.emit('disconnect')
