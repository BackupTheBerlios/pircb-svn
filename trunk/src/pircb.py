##################################
# (C) 2004 pIRCb                 #
# Python IRC Bot                 #
# Developed By:                  #
# (nick125) Nick                 #
##################################
# Released Under Terms of GPL    #
##################################
# Imports for needed modules

import socket
import string
import sys
import time
import fnmatch

# The Basic Authorization System (it uses hostmasks and passwords, :)

authorized = {}

identified = {}

def addUser(HOSTMASK, PASSWORD):
    if HOSTMASK.startswith("*!*@") == True:
         HOSTMASK = HOSTMASK[3:]
    elif HOSTMASK.startswith("@") == True:
         HOSTMASK = HOSTMASK[1:]
    authorized[HOSTMASK] = PASSWORD

# the function to identify users

def identifyUser(HOSTMASK, PASSWORD):
    if HOSTMASK.startswith("*!*@") == True:
         HOSTMASK = HOSTMASK[3:]
    elif HOSTMASK.find("@") > 0:
         HOSTMASK = HOSTMASK[HOSTMASK.find("@")+1:]
    print "%s requested auth" % (HOSTMASK)
    try:
         userpass = authorized[HOSTMASK]
         print "got pass from authorized db which is %s" % (userpass)
    except:
         userpass = ""    
    if userpass.lower() == PASSWORD.lower():
         identified[HOSTMASK] = "Y"
         return 1
         print "auth sucessful"
    elif userpass.lower() == PASSWORD.lower():
         return 0
         print "auth failed"
    else:
         print "auth went wrong"
         pass
# The Channel System. It keeps track of the channels

channels = []
numchan = 0
# the function to add a channel

def addchan(CHANNEL):
    channels.append(CHANNEL)

# the function to remove a channel

def delchan(CHANNEL):
    del channels[CHANNEL]

# setting up authorized users
#addUser("<hostmask>", "<password>")

# adding channels to join

#addchan("<channel>")

# the connection stuff
# in the future, this will be in a config file

# IRC Server Domain Name or IP Address (some way to get to the server)

SERVER = 'irc.freenode.net'

# port to attempt to connect to

PORT = 6667

# password that the server may need if you have a I:Line, if not, leave this blank

SVRPASSWORD = ''

# what do you want to call your bot? enter a nickname here!!

NICKNAME = 'pIRCb'

### DO NOT MODIFY BELOW THIS LINE OR ELSE I WILL COME AFTER YOU WITH A KNIFE!!!! ###


# very basic socket, multiple sockets for multiple server connection = future
IRCC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# uses the socket to make a connection to the server, duh
def connectServer():
    IRCC.connect((SERVER,PORT))

#ultra simple command to send data over the socket, under the bridge, and to the irc server
def sendIRC(command):
    IRCC.send(command + '\r\n')

# this joins the channels, enjoy!
def joinChannels():
    x = 0
    while (len(channels)-1 >= x):
	sendIRC("JOIN %s" % channels[x])
	x = x+1

def joinChannel(CHANNEL):
     channels.append(CHANNEL)
     sendIRC("JOIN %s" % (CHANNEL))
          
# send the login data or else!
def loginIRC(nickname, password="",username='pIRCb', servername=SERVER, realname='pIRCb', hostname="pIRCb"):
    # "to send a pass or not send a pass, that is the question"
    if password != "":
	# well, we have to send a pass, *sigh*, well, least it'll keep us busy
	sendIRC("PASS %s" % (password))
    elif password == "":
	# yey! no password! well, lets go farther!
        pass
    # well, the RFC-1459 says that i need to send this:
    #"USER <username> <hostname> <servername> <realname>" but i don't want to, /me don't want to
    sendIRC("USER %s %s %s %s" % (username, hostname, servername, realname))
    sendIRC("NICK %s" % (nickname))


# is the person authorized (and identified of course)? well, this function will tell you!

def authcheck(HOSTMASK):
    if HOSTMASK.startswith("*!*@") == True:
         HOSTMASK = HOSTMASK[3:]
    elif HOSTMASK.startswith("@") == True:
         HOSTMASK = HOSTMASK[1:]
    elif HOSTMASK.find("@") > 0:
         HOSTMASK = HOSTMASK[HOSTMASK.find("@")+1:]
    try:
        identified[HOSTMASK]
        return 1
    except:
        return 0

# This function will check if the channel is one the bot has joined, if so, it will return 1

def inchan(CHKCHANNEL):
    if CHKCHANNEL.startswith("#") == True:
         VALID=1
    elif CHKCHANNEL.startswith("@") == True:
         VALID=1
    else:
         VALID=0
    try:
        stat = channels[CHKCHANNEL]
    except:
        stat = ""
    if stat == "":
        return 0
    elif stat == "y":
        return 1
    elif stat == "n":
        return 0
    else:
        return 0                        

# the message parser

def mesparse(message):
   try:
       callsig = "!"
       if message[0] == "PRIVMSG" and message[1] == NICKNAME:
           pm = 1
       elif message[0] == "PRIVMSG" and message[1] != NICKNAME:
           pm = 0
       # getting hostmask for and possible later usage (such as in kick, etc)
       HOSTMASK = string.lstrip(message[0], ':')
       # getting the nick name of the victims......i meant users, dangit!
       nick_name = string.lstrip(msg[0][:string.find(message[0],"!")], ':')
       
       if message[2] != NICKNAME:
           CHANNEL = message[2]
       else:
           CHANNEL = nick_name
       if string.upper(string.lstrip(msg[3], ':')) == string.upper('%ssay' % (callsig)):
           strsnd = message[4:55]
           strsnd = ' '.join(strsnd)
           sendIRC("PRIVMSG %s :%s Said: %s" % (CHANNEL, nick_name, strsnd))
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%stell' % (callsig)):
           sndto = message[4]
           strsnd = message[5:50]
           strsnd = ' '.join(strsnd)
           sendIRC("PRIVMSG %s :%s told me to tell you: %s" % (sndto, nick_name, strsnd))
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%sjoin' % (callsig)):
           chkauth = authcheck(HOSTMASK)
           chan = msg[4]
           if chkauth == 0:
               sendIRC("PRIVMSG %s :%s: You Are Not Identified" % (nick_name, nick_name))
           #elif chkauth == 1:
           #   sendIRC("PRIVMSG %s :%s: Authorization Failed" % (nick_name, nick_name))
           elif chkauth == 1:
               joinChannel(chan)
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%sidentify' % (callsig)):
           user = nick_name
           password = msg[4]
           idstat = identifyUser(HOSTMASK, password)
           if int(idstat) == 0:
               sendIRC("PRIVMSG %s :%s: Identification Failed" % (user, user))
           if int(idstat) == 1:
               sendIRC("PRIVMSG %s :%s: Identification Was Successful" % (user, user))
           else:
               sendIRC("PRIVMSG %s :%s: Error Happened!" % (user, user))
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%spart' % (callsig)):
           chkauth = authcheck(HOSTMASK)
           chan = msg[4]
           
           if chkauth == 0:
               sendIRC("PRIVMSG %s :%s: You Are Not Identified" % (nick_name, nick_name))
           #elif chkauth == 1:
           #   sendIRC("PRIVMSG %s :%s: Authorization Failed" % (nick_name, nick_name))
           elif chkauth == 1:
               sendIRC("PART %s :Parted From %s by %s" % (chan, chan,nick_name))
       
       # the quit function

       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%squit' % (callsig)):
           chkauth = authcheck(HOSTMASK)
           
           if chkauth == 0:
               sendIRC("PRIVMSG %s :%s: You Are Not Identified" % (nick_name, nick_name))
           #elif chkauth == 1:
           #   sendIRC("PRIVMSG %s :%s: Authorization Failed" % (nick_name, nick_name))
           elif chkauth == 1:
	       sendIRC("QUIT :Quit Signal Recived from %s" % (nick_name)) 
               time.sleep(10)
               IRCC.close()
               sys.exit(0)
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%skick' % (callsig)):
        
           chkauth = authcheck(HOSTMASK)
           kicked = msg[4]
           try:
               reason = msg[5:]
               reason = ' '.join(reason)
           except:
               reason = "You Have Been Naughty"
           if reason == "":
               reason = "You Have Been Naughty"
           if chkauth == 0:
               sendIRC("PRIVMSG %s :%s: You Are Not Identified" % (nick_name, nick_name))
           #elif chkauth == 1:
           #   sendIRC("PRIVMSG %s :%s: Authorization Failed" % (nick_name, nick_name))
           elif chkauth == 1:
               sendIRC("KICK %s %s :Kicked by %s: %s" % (CHANNEL,kicked,nick_name,reason))  
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%sop' % (callsig)):   
           chkauth = authcheck(HOSTMASK)
           try:
               person = msg[4]
           except:
               person = nick_name
           if chkauth == 0:
               sendIRC("PRIVMSG %s :%s: You Are Not Identified" % (nick_name, nick_name))
               if person.lower() == NICKNAME.lower():
                   sendIRC("PRIVMSG %s :%s: Hmm, Don't I Need To Be Op'ed to Op Myself?" %(nick_name, nick_name))
           #elif chkauth == 1:
           #   sendIRC("PRIVMSG %s :%s: Authorization Failed" % (nick_name, nick_name))
           elif chkauth == 1:
               if person.lower() == NICKNAME.lower():
                   sendIRC("PRIVMSG %s :%s: Hmm, Don't I Need To Be Op'ed to Op Myself?" %(nick_name, nick_name))
               else:
                   sendIRC("MODE %s +o %s" % (CHANNEL, person))
       elif string.upper(string.lstrip(msg[3], ':')) == string.upper('%sstats' % (callsig)):
           cpuse = time.clock()
           usestr = "pIRCb Version 0.1 SVN :.:.: Bot Nick: %s :.:.: Number Of Channels: %s :.:.: Number Of Functions Operated: %s :.:.: CPU Usage: %s" % (NICKNAME, len(channels), 0, cpuse)
           sendIRC("PRIVMSG %s :%s" % (CHANNEL, usestr))  
   except:
        pass
connectServer()
print "connected to server"
time.sleep(2)
loginIRC("pIRCb")
print "logged in"
joinChannels()
while True:
    try:
        try:
            buffer = IRCC.recv(16*5000)
            msg = string.split(buffer)
            if msg[0] == "PING": # check if the irc server wants a response, if so, SEND IT!!!!!!
	        sendIRC("PONG %s" % msg[1]) # answer!!!!! YEY!!!
            elif msg[1] == 'KICK':
    	        print ":)"
	        #More to come here
            else:
                mesparse(msg)
        except:
            pass
    except KeyboardInterrupt:
         sys.exit(0)
