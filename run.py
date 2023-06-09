'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

#-----------------------------------------------------------------------------
import os
import sys
import socket
import gunicorn
import sql
from gevent import monkey; monkey.patch_all()
from bottle import run

#-----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load 
# Each file separately

# For the template, we will keep them together

import model
import view
import controller

#-----------------------------------------------------------------------------

# It might be a good idea to move the following settings to a config file 
# and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = '127.0.0.1'

# Test port, change to the appropriate port to host
sock = socket.socket()
sock.bind(('', 0))
port = sock.getsockname()[1]
sock.close()
#port = 8081

# Turn this off for production
debug = True

def run_server():    
    '''
        run_server
        Runs a bottle server
    '''
    run(host=host, port=port, debug=debug, interval=10, server='gevent', 
        reloader=False, certfile='./certificates/localhost.crt', 
        keyfile='./certificates/localhost.key')
    
def manage_db():
    '''
        manage_db
        Starts up and re-initialises an SQL databse for the server
    '''
    database_args = ":sql.db:"
    sql_db = sql.SQLDatabase(database_args)

    return

def wipe_db():
    '''
        wipe_db
        Wipe everything on SQL database
    '''
    database_args = ":sql.db:"
    sql_db = sql.SQLDatabase(database_args)
    sql_db.database_wipe()
    print("All data wiped.")

    return

#-----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db' : manage_db,
    'server'       : run_server,
    'wipe_db' : wipe_db
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

run_commands(sys.argv)