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

To run click client:
cd to the click directory
enter the virtual environment
type "athena" to read help info

Protocol
--------
Initially, the server host starts the "Athena" service by listening with
socket.IO on port 5000 (or designated port).  When a client host wishes
to make use of the service, it establishes a connection with the server
host. The client and Athena server will exchange commands and responses
(respectively) until the connection is closed or aborted.

Commands consist of a custom event keyword, possibly followed by one or
more arguments in the form of a python dictionaries or json. For every command
the client will receive a responses from the server with a custom event
handle and either a string or a json. To prevent unauthorized use the client my proved a valid user name and password with all communication.

The client can request scores for a specific game by sending an emit
with the custom event handle ‘get_score’ with a python dictionary containing the keys nickname, password, and game name. The client will receive a custom event handle 'get_score_response' containing a json with the key 'msg' and a message. The client can submit a flag by sending an emit with the custom event handle 'submit_flag' with a python dictionary containing the users nickname, password, game name,flag name, and flag value. The client will receive a custom event handle 'submit_flag_response' containing a json with the key 'msg' and value message. The client can request games he/she is registered in by sending an emit with keys nickname and password. The client will receive a custom event handle 'get_game_response containing a json with the key 'msg' and value message. The client can request scoreboards he/she for a game they are registered in by sending an emit with the keys nickname and password. The client will recieve a custom event handle 'get_scoreboard_reponse' containing a json with the key 'msg' and value message. 
Licensing
---------
N/A at this time.

Copyright
---------
N/A at this time.

Contacts
--------
Jan Masztal janmasztal@mail.adelphi.edu



