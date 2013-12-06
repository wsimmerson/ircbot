#!/usr/bin/python3

import sys
import socket
import string
import argparse
import logging

class ircbot(object):
	"""
		Object to handle a IRC session
	"""

	def __init__(self):
		self.HOST = "irc.freenode.net"
		self.PORT = 6667
		self.CHANNEL = "#SomeChannel"
		self.NICK = "[Asimov]"
		self.IDENT = "[Asimov]"
		self.REALNAME = "[Asimov]"
		self.MASTER = "Username" # User that can give administrative commands

		self.irc = socket.socket()
		self.irc.connect((self.HOST, self.PORT))
		logging.debug("Connect %s:%s" % (self.HOST, str(self.PORT)))

		self.irc.send(bytes("NICK %s\r\n" % self.NICK))
		self.irc.send(bytes("USER %s %s bla :%s\r\n" % (self.IDENT,
														self.HOST,
														self.REALNAME)))
		logging.debug("USER %s %s bla :%s" % (self.IDENT, self.HOST, self.REALNAME))
		self.irc.send(bytes("JOIN %s\r\n" % self.CHANNEL))
		self.irc.send(bytes("PRIVMSG %s :Hello Master\r\n" % self.MASTER))
		logging.debug("PRIVMSG %s :Hello Master" % self.MASTER)

	def priv_from_master(self, line):
		"""
			True / False identify private messages from master
		"""
		if self.MASTER in line[0] and 'PRIVMSG' in line[1] and self.NICK in line[2]:
			return True
		else:
			return False

	def handle_master_commands(self, line):
		"""
			Parses command line and handles accordingly
		"""
		if line[3].lower() == ':speak' and len(line) > 4:
			msg = ' '.join(line[4:len(line)])
			self.irc.send(bytes("PRIVMSG %s :%s\r\n" % ( self.CHANNEL, msg)))

	def run(self):
		"""
			Main Application Loop
		"""
		readbuffer = ""

		while True:
			readbuffer = readbuffer + self.irc.recv(1024).decode('utf-8')
			temp = readbuffer.split("\n")
			logging.debug(readbuffer)
			readbuffer = temp.pop()


			for line in temp:
				linex = line.rstrip()
				linex = linex.split()

				if (linex[0] == "PING"):
					self.irc.send(bytes("PONG %s\r\n" % linex[1]))
					logging.debug("PONG %s" % linex[1])

				elif self.priv_from_master(linex):
					logging.debug("Message from Master logged")
					self.handle_master_commands(linex)

				elif "three laws" in ' '.join(linex[3:len(linex)]).lower():
					self.irc.send(bytes("PRIVMSG %s :%s\r\n" % (self.CHANNEL, "Law 1: A robot may not injure a human being or, through inaction, allow a human being to come to harm.")))
					self.irc.send(bytes("PRIVMSG %s :%s\r\n" % (self.CHANNEL, "Law 2: A robot must obey the orders given to it by human beings, except where such orders would conflict with the First Law.")))
					self.irc.send(bytes("PRIVMSG %s :%s\r\n" % (self.CHANNEL, "Law 3: A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.")))

def parseargs():
	"""
		Optional Debugger action
	"""

	parser = argparse.ArgumentParser()
	parser.add_argument("--debug", default=False, action='store_true', help='debug this shit')
	
	return parser.parse_args()


if __name__ == '__main__':

	# Debugger Options
	opt = parseargs()
	if opt.debug:
		logging.basicConfig(level=logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO)

	# Run the Bot
	bot = ircbot()
	bot.run()
 
