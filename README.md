Athena
---------

What is it?
-----------
An early development of a web-based scoreboard application for
capture-the-flag games that will be able to communicate with
multiple clients. The primary function of this web application is to
host scoreboards. Other features include user/game registration,
login/authentication, downloads, update game information, and
news.

The clients that connects to the web application will be responsible
for retrieving players scores, accepting flags from players,
calculating points, and sending updated scores to the web application
scoreboards.

The Latest Version
------------------
Currently in early Alpha.


Documentation
-------------
Currently run on Ubuntu 14.04
The web application currently allows a user signup and login/logout.
Once a user is logged in they can view and edit their own profile as
well as view other user profiles. They are able to view the home,
scoreboard,games, and download pages. These web pages are
currently minimalistic at best.

There is no distinction between user privileges.

The simple client application will update current users scores for
games they are currently associated with.

Installation
------------
Required Packages:
python
sqlite3
python-vitualenv
python-dev

Web server:
Download and extract package.
cd into the root directory and run '. flask/bin/activate'
run './run.py'

If you receive errors install the following:
(packages should already be installed in flask/bin/activate)
pip install flask
pip install flask-login
pip install flask-openid
pip install flask-sqlalchemy
pip install sqlalchemy-migrate
pip install flask-whooshalchemy
pip install sqlalchemy-migrate
pip install flask-whooshalchemy
pip install flask-wtf
pip install flask-socketio

re-run './run.py'
open browser to 127.0.0.1:5000

To run simple client (located in the clients directory):
run 'VIRTUAL_ENV=$HOME/.virtualenv;virtualenv $VIRTUAL_ENV;source $VIRTUAL_ENV/bin/activate;pip install -U socketIO-client'

edit simple_client.py as you wish.
To run 'python simple_client.py'

Protocol
--------
First Draft.(expandable)
The first draft of the protocol is meant to be simple and will be
expanded upon through the duration of the project.

Initially, the server host starts the "Athena" service by listening with
socket.IO on port 5000 (will change port).  When a client host wishes
to make use of the service, it establishes a connection with the server
host. When the connection is established, the "Athena" server sends a
greeting (not yet working). The client and Athena server then exchange
commands and responses (respectively) until the connection is closed or
aborted.

Commands consist of a custom event keyword, possibly followed by one or
more arguments in the form of a python dictionaries or json. For every command
the client will receive a responses from the server with a custom event
handle and either a string or a json. The client will verify connection by
sending an emit with a custom event handle 'connect'. If the client is
connected to the server the client will receive the a custom event handle
'connect_response' containing a json with the key 'data' and value
'User Connected'.

The client can request scores for a current player by sending an emit
with the custom event handle ‘score_request’ with a python dictionary
containing the keys nickname, game, authentication with thier respected
values. The client will receive a custom event handle 'score_response'
containing a json with the key 'score' and the score value. The client can
update a users score by sending an emit with the custom event handle
'score_update' with a python dictionary containing the users nickname
game name,score, and authentication along with the respective values.
The client will receive a custom event handle 'updated_score' containing
a json with the key 'score' and value 'Score Updated'. 
Licensing
---------
N/A at this time.

Copyright
---------
N/A at this time.

Contacts
--------
Jan Masztal janmasztal@mail.adelphi.edu



