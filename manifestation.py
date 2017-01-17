from __future__ import print_function

import os
import time
import socket
import string
import subprocess

with open("corpus", "w") as f:
    f.write(str(os.getpid()))

import dicongwochomut.spark

def parsemsg(s):
    # Stolen from Twisted. Parses a message to it's prefix, command and arguments.
    prefix = ''
    trailing = []
    if s == "":
        print("Empty line. (something bad happened)")
    if s[0] == ':':
        prefix, s = s[1:].split(' ', 1)
    if s.find(' :') != -1:
        s, trailing = s.split(' :', 1)
        args = s.split()
        args.append(trailing)
    else:
        args = s.split()
    command = args.pop(0)
    return prefix, command, args


def isNumber(s):
    # Returns true if s is a number, false if not
    try:
        int(s)
        return True
    except ValueError:
        return False


class Bot:
    def __init__(self, host='eu.sorcery.net', port=9000):
        self.host = host
        self.port = port

        self.nickName = 'DicongwoChomut'
        self.ident = 'DicongwoChomut'
        self.realName = 'DicongwoChomut'

        self.receiveBuffer = ""

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.scrying = False
        self.querent = ("", "")
        self.sigilpath = os.getcwd()+"/sigil"

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.socket.send("NICK %s\r\n" % self.nickName)
        self.socket.send("USER %s %s bla :%s\r\n" % (self.ident, self.host, self.realName))

    def send(self, msg):
        self.socket.send('{0}\r\n'.format(msg).encode())

    def sendMsg(self, chan, msg):
        sendString = "PRIVMSG "+chan+" :"+msg
        self.send(sendString)

    def receive(self):
        self.receiveBuffer = ""
        try:
            self.receiveBuffer=self.socket.recv(1024)
        except socket.error, e:
            if e.args[0] != 11:
                # We don't just have a "no data received" error
                with open("errors", "w") as f:
                    print(e, file=f)
                sys.exit(1)
        temp=string.split(self.receiveBuffer, "\n")
        for line in temp:
            try:
                line=string.rstrip(line)
                line=string.split(line)
            
                if(line[0]=="PING"):
                    self.socket.send("PONG %s\r\n" % line[1])
            except:
                pass


    def join(self, channel):
        self.socket.send("JOIN {} \r\n".format(channel))

    def handleInput(self):
        if len(self.receiveBuffer) > 0:
            # OVERRIDE THIS FUNCTION
            prefix, command, args = parsemsg(self.receiveBuffer)

            if command == "PRIVMSG":
                channel = args[0]

                inputString = args[1]
                inputString = inputString[:-2]
                if self.nickName in inputString:
                    if self.scrying:
                        self.sendMsg(channel, "Please wait, I am currently occupied with "+self.querent[1]+"'s target.")
                    else:
                        self.scrying = True
                        self.querent = (channel, prefix[:prefix.index("!")])
                        with open("target", "w") as f:
                            f.write(inputString)
                        subprocess.call("./draw.sh")

    def uploadsigil(self):
        if os.path.exists(self.sigilpath):
            with open(self.sigilpath, "r") as f:
                link = f.read()
            self.sendMsg(self.querent[0], self.querent[1]+": "+link)
            # Clean up
            self.querent = ("", "")
            self.scrying = False
            os.remove(self.sigilpath)


bot = Bot()
bot.connect()
time.sleep(2)
bot.join("#/div/ination")
bot.socket.setblocking(False)
while True:
    bot.receive()
    bot.handleInput()

    try:
        with open("life", "r") as f:
            pass
    except:
        import sys
        sys.exit(1)

    if bot.scrying:
        bot.uploadsigil()
