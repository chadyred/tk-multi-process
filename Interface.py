# -*- coding: utf-8 -*-
#
#  PyConnect.py
#
# Vérification de la connexion internet avec interface et ping
#
 
#Importation des librairies nécéssaire au bon fonctionnement du programme.
#Tkinter pour l'interface graphique
#urllib pour les schémas internet
#os pour dialoguer avec le systeme
from tkinter import *
import urllib as url
import os 
import subprocess 
import shlex 
from threading import Thread
from multiprocessing import Queue
from queue import Empty

class Interface(Frame):
	def __init__(self,parent):
		Frame.__init__(self)
		self.parent = parent
		self.outputCommand = ""
		self.etat = Label(self, text='',font='Times 28 italic bold')
		self.etat.grid(row=0, column=0, columnspan=4, sticky=NSEW)
 
		self.lab_iface = Label(self, text='Interfaces:',font='Times',underline=0)
		self.lab_iface.grid(row=1,column=0,sticky=NSEW)
 
		self.iface = Text(self, font='Times 10')
		self.iface.grid(row=2, column=0, sticky=NSEW)
 
		self.lab_ping = Label(self, text='Ping:',font='Times',underline=0)
		self.lab_ping.grid(row=1,column=2,sticky=NSEW)

		self.ping = Text(self, font='Times',state='disabled')
		self.ping.grid(row=2, column=1, columnspan=3, sticky=NSEW)
 
		self.recharger = Button(self, text='Recharger', font='Times', command=self.checkIface)
		self.recharger.grid(row=3, column=0, sticky=NSEW)
 
		self.quitter = Button(self, text='Quitter', font='Times', command=self.leave)
		self.quitter.grid(row=3, column=1, columnspan=3,sticky=NSEW)
 
		# self.checkIface()
 
	def checkIface(self):
		self.iface.config(state='normal')
		self.checkInternet()
		self.startProcess('make help')
 
	def checkInternet(self):
		try:
			url.urlopen('http://www.google.com')
			self.etat.config(text='Connexion internet active')
			self.checkPing()
		except:
			self.etat.config(text='Connexion internet inactive')
			self.ping.config(state='normal')
			self.ping.delete(1.0,END)
			self.ping.insert(END, 'Ping impossible...')
			self.ping.config(state='disabled')
 
	def checkPing(self):
		self.ping.config(state='normal')
		self.ping.delete(1.0,END)
		c = 3
		while c != 0:
			self.pingPacket = os.popen('ping -c 1 google.com').read()
			self.ping.insert(END, self.pingPacket+'\n')
			self.parent.after(1,self.parent.update())
			c = c-1
 
		self.ping.config(state='disabled')
 	
	def readlines(self, process, queue):
		"""Lecture de la dépilationd e la sortie standard"""

		while process.poll() is None:
			queue.put(process.stdout.readline())

		print(str(self.queue.qsize()))

	def startProcess(self, command):
		"""Fonction qui sera lancé afind e récupérer la sortie standard"""

		self.process = subprocess.Popen(shlex.split(command),
			stdout=subprocess.PIPE,
			stdin=subprocess.PIPE,
			stderr=subprocess.PIPE)

		self.queue = Queue()
		# Le thread exécutera la fonction target avec le processus et la file d'attente
		self.thread = Thread(target=self.readlines, args=(self.process, self.queue))
		self.thread.start()

		self.after(1000, self.updateLines)

	def updateLines(self):
		"""Fnction va permettre de paramétrer l'affichage des ligne au seind de l'interface"""

		# self.iface.delete(1.0,END)

		try:
			print("Try : " + str(self.queue.qsize()))
			line = self.queue.get() # False for non-blocking, raises Empty if empty
			self.iface.config(state='normal')
			self.iface.insert(END, line)
			# self.iface.config(state='disabled')
		except Empty:
			print('Empty')
			pass

		if self.process.poll() is None:
			print("Poll")
			self.after(100, self.updateLines)

	def leave(self):
		quit()