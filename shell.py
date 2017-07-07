import os
import sys
import subprocess
directory = os.getcwd()

def parser(command):
	commandl = []
	outdir = ""
	indir = ""
	waiting = False
	if '&' in command:
		waiting = True
		command = command.replace("&", "")
	if '>' in command:
		outdir = command[command.find('>')+2::]
		outdir = outdir[:outdir.find(' '):]
		command = command.replace("> {} ".format(outdir), "")
	if '<' in command:
		indir = command[command.find('<')+2::]
		indir = indir[:indir.find(' '):]
		command = command.replace("< {} ".format(indir), "")
		
	command = command.split("|")
	for i in range(len(command)):
		command[i] = command[i].split(' ')
		while '' in command[i]:
			command[i].remove('')
			
	commandl = command
	
	return commandl, outdir, indir, waiting
	
def commandfinder(command):
	path = os.environ["PATH"]
	path = path.split(':')
	if '/' in command[0]:
		return command
	else:
		for i in path:
			if(os.path.isfile("{}/{}".format(i,command[0]))):
				command[0] = i + '/' + command[0]
				return command
	
def interpreter(commandl, outdir, indir, waiting):
	try:
		inp=subprocess.PIPE
		if bool(indir):
			a = open(indir, "r")
		if bool(outdir):
			b = open(outdir, "w")
		for command in commandl:
			if(command[0] == "cd"):
				os.chdir(command[1])
			else:
				if bool(indir):
					if command == commandl[0]:
						p1 = subprocess.Popen(commandfinder(command), stdin=a, stdout=subprocess.PIPE)
						inp = p1.stdout
					else:
						p1 = subprocess.Popen(commandfinder(command), stdin=inp, stdout=subprocess.PIPE)
						inp = p1.stdout
				else:
					if command == commandl[0]:
						p1 = subprocess.Popen(commandfinder(command), stdin=sys.stdin, stdout=subprocess.PIPE)
						inp = p1.stdout
					else:
						p1 = subprocess.Popen(commandfinder(command), stdin=inp, stdout=subprocess.PIPE)
						inp = p1.stdout
		if(type(inp) is not int):
			if bool(outdir):
				b.write((inp.read()).decode("utf-8"))
			else:
				os.write(1,inp.read())
	except:
		print("Comando nao reconhecido")

while True:

	command = input("{} >> ".format(directory))
	if command == "exit":
		break
	commandl, outdir, indir, waiting = parser(command)
	interpreter(commandl, outdir, indir, waiting)
	directory = os.getcwd()
	
