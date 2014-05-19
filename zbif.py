#!/usr/bin/python
# -*- coding: UTF8 -*-

# Adrien KERFOURN
# 08/08/2012

import math

zbiferrmsg = {}
zbiferrmsg["unknow"] = "Unknow error."
zbiferrmsg["nocol"] = "No columns in the data file detected."

class zbifError(Exception):
	def __init__(self,err,plus=""):
		self.err = err
	def __str__(self):
		return zbiferrmsg[self.err].format(self.plus)

class zbif:
	def __init__(self,fin,fout,skip=0,sigfig=-1,bufsize=30):
		self.setskip(skip)
		self.setsigfig(sigfig)
		self.setbufsize(bufsize)

		if type(fin)==str:
			self.fin = open(fin,'r')
		else:
			self.fin = fin
		if type(fout)==str:
			self.fout = open(fout,'w')
		else:	
			self.fout = fout
	
	def setskip(self, skip):
		if skip < 0:
			self.skip = 0
		else:
			self.skip = skip
	
	def setsigfig(self, sigfig):
		self.sigfig = sigfig
		
	def setbufsize(self, bufsize):
		if bufsize < 0:
			self.bufsize = 0
			self.buflist = []
		else:
			self.bufsize = bufsize
			self.buflist = []
			i = 0
			while i < bufsize:
				self.buflist.append("")
				i+=1
		self.bufindex = 0
					
	def zip(self):
		cnt = 0
		for line in self.fin:
			if cnt <= 0:
				lw = ""
				col = line.strip().split()
				i = 0
				if len(col) > 0:
					lw += sstropt(float(col[0]),self.sigfig)
					i+=1
					while i < len(col):
						lw += " "+sstropt(float(col[i]),self.sigfig)
						i+=1
					if lw not in self.buflist:
						self.fout.write(lw+"\n")
						if self.bufsize > 0:
							self.buflist[self.bufindex] = lw
							self.bufindex = (self.bufindex + 1) % self.bufsize
				else:
					raise zbifError("nocol")
				cnt = cnt + self.skip
			else:
				cnt = cnt - 1

#--- Function ---

def frexp10(x,n=-1):
		s = 1
		if x < 0:
			s = -1
			x = -x
		if x != 0:
			exp = math.log10(x)
			e = int(math.floor(exp))
			m = s*math.pow(10,exp-e)
			if n < 0:
				return (m,e)
			else:
				return (round(m,n),e)
		else:
			return (0.0,1)

def mestr(m,e):
	if e != 0:
		return str(m) + "e" + str(e)
	else:
		return str(m)

def mestropt(m,e):
	if (e < -2) or (e > 1):
		return str(m) + "e" + str(e)
	elif e != 0:
		return str(m * math.pow(10,e))
	else:
		return str(m)

def mestrfull(m,e):
	return str(m*math.pow(10,e))

def sstr(x,n=-1):
	(m,e) = frexp10(x,n)
	return mestr(m,e)

def sstropt(x,n=-1):
	(m,e) = frexp10(x,n)
	return mestropt(m,e)

def sstrfull(x,n=-1):
	(m,e) = frexp10(x,n)
	return mestrfull(m,e)


if __name__=="__main__" :
	import argparse
	import os

	parser = argparse.ArgumentParser(prog="zbif",version="0.9",add_help=True,description="Optimisation du fichier de donnée pour l\'affichage de diagrammes de bifurcations.")
	
	parser.add_argument('-in','-i', action="store", dest="inputfile", help="Nom du fichier d'entrée.", default=None)
	parser.add_argument('-out','-o', action="store", dest="outputfile", help="Nom du fichier de sortie.", default=None)
	parser.add_argument('--buffersize','-bs', action="store", dest="bufsize", help="Taille du buffer utilisé pour l'optimisation des données (30 par défaut).", default=30,type=int)
	parser.add_argument('--skipdata','-sd', action="store", dest="Nskip", help="Pour 1 ligne de traitée, les Nskip lignes suivantes sont ignorées (0 par défaut).", default=0,type=int)
	parser.add_argument('--sigfigs','-sf', action="store", dest="sigfigs", help="Impose le nombre de chiffres significatifs (=SIGFIGS+1) maximum pour l'affichage (-1 par défaut).\n Note : plus le nombre de chiffres significatifs est faible plus le programme pourra optimiser les données, il faut donc trouver un compromis entre la taille du fichier de sortie et la précision d'affichage souhaitée.\n Note 2 : Une valeur négative indique que le programme ne tronquera pas les données.", default=-1,type=int)
	parser.add_argument('-io', action="store",dest="iofile",help="Allows to have the same file in input and output.",default=None)

	args = vars(parser.parse_args())

	isio = False

	if args["iofile"] != None:
		isio = True
		args["inputfile"] = args['iofile']
		args["outputfile"] = args['iofile']+".tmp"

	try:
		fin = open(args["inputfile"],'r')
	except IOError:
		print "Error : the file "+args["inputfile"]+" does not exist."
	try:
		fout = open(args["outputfile"],'w')
	except IOError:
		print "Error : the file "+args["outputfile"]+" can't be open or created."

	sigfig = int(args["sigfigs"])			# nombre de chiffres significatifs
	skip = int(args["Nskip"])
	bufsize = int(args["bufsize"])			#buffer size

	try:
		zipbif = zbif(fin,fout, skip, sigfig, bufsize)
		zipbif.zip()
	except zbifError as e:
		print "Error : " + str(e)

	fin.close()
	fout.close()

	if isio:
		os.rename(args["outputfile"],args["inputfile"])

