import os

def err(text):
	try:
		f=open('err.txt','a')
		f.write(str(text)+'\n\n')
		f.close()
	except:
		f=open('err.txt','w')
		f.write(str(text)+'\n\n')
		f.close()


def log(text):
	try:
		f=open('log.txt','a')
		f.write(str(text)+'\n\n')
		f.close()
	except:
		f=open('log.txt','w')
		f.write(str(text)+'\n\n')
		f.close()


def clear():

	os.system('cls' if os.name=='nt' else 'clear')
