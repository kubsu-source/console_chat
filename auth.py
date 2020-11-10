import hashlib

from additional import *

def hashing(passwd,hashing='sha512'):
	#hash password
	return hashlib.sha512(passwd.encode('utf-8')).hexdigest()


def get_passwd(labels,keyWord):
	while True:
		passwd=['',0,False]
		result=''
		print(space+styleDef+foreMain+keyWord+foreSub,end='\r')
		while True:
			key = msvcrt.getwch()
			num = ord(key)
			
			if num==27:
				#ESC
				pass
			elif num==224:
				key = msvcrt.getwch()
				num = ord(key)
				if num==71:
					pass
			elif num==8:
				if len(passwd[0])!=0:
					if passwd[0][len(passwd[0])-1]==' ' and passwd[2]==True:
						passwd[0]=passwd[0][:-1]
				passwd[0]=passwd[0][:-1]
				passwd[0]+=' '
				passwd[1]-=1
				passwd[2]=True
				result=result[:-1]
			elif num==13:
				#enter
				print(space+styleDef+foreMain+keyWord+foreSub+passwd[0])
				break
			elif key==' ':
				if len(passwd[0])!=0:
					if passwd[0][len(passwd[0])-1]==' ' and passwd[2]==True:
						passwd[0]=passwd[0][:-1]
						passwd[2]=False
				passwd[0]+='*'
				result+=' '
			elif key=='shift' or key=='alt' or key=='ctrl':
				pass
			else:
				if len(passwd[0])!=0:
					if passwd[0][-1]==' ' and passwd[2]==True:
						passwd[0]=passwd[0][:-1]
						passwd[2]=False
				passwd[0]+='*'
				result+=key
			
			x,y,curl,bottom=get_window_params()
			cursor.hide()
			print(space+styleDef+foreMain+keyWord+foreSub+passwd[0],end='\r')
		if result=='':
			print(space+styleDef+foreMain+dictionary['Type something!'][language])
			sleep(1)
			clear()
			for label in labels:
				print(space+styleDef+foreMain+label[0]+foreSub+label[1])
			continue
		else:
			break

	return result


def sign_up():
	foreMain, foreMain_, foreSub, foreSub_, styleDef, styleDef_, space, space_, language, language_=check_config()
	while True:
		clear()
		print(space+styleDef+foreMain+dictionary['Login: '][language]+foreSub,end='')
		login=input()
		print(space+styleDef+foreMain+dictionary['Loading ...'][language],end='\r')
		if not login:
			print(space+styleDef+foreMain+dictionary['Type something!'][language])
			sleep(1)
		elif login==SYSTEM_NAME:
			print(space+styleDef+foreMain+dictionary['You cannot choose this name!'][language])
			sleep(1)
		else:
			again=False
			check=firebase.get('/'+encode_str('users'), None)
			if check==None:
				break
			for i in check.keys():
				if decode_str(i)==login:
					again=True
					print(space+styleDef+foreMain+dictionary['This name is taken!'][language])
					sleep(1)
					break
			if again==False:
				break
	while True:
		print(space+styleDef+foreMain+' '*len(dictionary['Loading ...'][language]),end='\r')
		print(space+styleDef+foreMain+dictionary['Email: '][language]+foreSub,end='')
		email=input()
		if not email:
			print(space+styleDef+foreMain+dictionary['Type something!'][language])
			sleep(1)
			clear()
			print(space+styleDef+foreMain+dictionary['Login: '][language]+foreSub+login)
			continue
		else:
			break
	while True:
		passwd=get_passwd([[dictionary['Login: '][language],login],[dictionary['Email: '][language],email]],dictionary['Password: '][language])
		repeat=get_passwd([[dictionary['Login: '][language],login],[dictionary['Email: '][language],email],[dictionary['Password: '][language],('*'*len(passwd))]],dictionary['Repeat password: '][language])

		if passwd!=repeat:
			print(space+styleDef+foreMain+dictionary['Passwords are not equel!'][language])
			sleep(1)
			clear
		else:
			passwd=hashing(passwd)
			break
	
	print(space+styleDef+foreMain+'\n'+dictionary['Loading ...'][language])
	data={encode_str('hash'):encode_str(passwd),encode_str('email'):encode_str(email)}
	result=firebase.patch('/'+encode_str('users')+'/'+encode_str(login), data)
	myName=login
	return 'menu',myName


def sign_in():
	foreMain, foreMain_, foreSub, foreSub_, styleDef, styleDef_, space, space_, language, language_=check_config()
	myName=''
	while True:
		clear()
		print(space+styleDef+foreMain+dictionary['Login: '][language]+foreSub,end='')
		login=input()
		if login=='':
			print(space+styleDef+foreMain+dictionary['Type something!'][language])
			sleep(1)
		elif login==SYSTEM_NAME:
			print(space+styleDef+foreMain+dictionary['You cannot choose this name!'][language])
			sleep(1)
		else:
			break
	passwd=get_passwd([[dictionary['Login: '][language],login]],dictionary['Password: '][language])
	passwd=hashing(passwd)
	print('\n'+space+styleDef+foreMain+dictionary['Loading ...'][language])

	data={encode_str('name'):encode_str(login),encode_str('hash'):encode_str(passwd)}

	check=firebase.get('/'+encode_str('users'), None)
	if check==None:
		while True:
			print(space+styleDef+foreMain+dictionary['No such account!'][language])
			print(space+styleDef+foreMain+dictionary['Create new? (y/n): '][language],end='')
			ans=input().lower()
			if ans=='y' and language==LANGUAGE.index('English') or ans=='д' and language==LANGUAGE.index('Russian'):
				return 'sign_up', myName
			elif ans=='n' and language==LANGUAGE.index('English') or ans=='н' and language==LANGUAGE.index('Russian'):
				return 'sign_in', myName
			else:
				print(space+styleDef+foreMain+dictionary['No such option!'][language])
				sleep(1)
				clear()

	for i in check.keys():
		if decode_str(i)==login and decode_str(check[i][encode_str('hash')])==passwd:
			myName=login
			return 'menu', myName
		elif decode_str(i)==login:
			while True:
				print(space+styleDef+foreMain+dictionary['Wrong password!'][language])
				print(space+styleDef+foreMain+dictionary['Create new? (y/n): '][language],end='')
				ans=input().lower()
				if ans=='y' and language==LANGUAGE.index('English') or ans=='д' and language==LANGUAGE.index('Russian'):
					return 'sign_up', myName
				elif ans=='n' and language==LANGUAGE.index('English') or ans=='н' and language==LANGUAGE.index('Russian'):
					return 'sign_in', myName
				else:
					print(space+styleDef+foreMain+dictionary['No such option!'][language])
					sleep(1)
					clear()
	while True:
		print(space+styleDef+foreMain+dictionary['No such account!'][language])
		print(space+styleDef+foreMain+dictionary['Create new? (y/n): '][language],end='')
		ans=input().lower()
		if ans=='y' and language==LANGUAGE.index('English') or ans=='д' and language==LANGUAGE.index('Russian'):
			return 'sign_up', myName
		elif ans=='n' and language==LANGUAGE.index('English') or ans=='н' and language==LANGUAGE.index('Russian'):
			return 'sign_in', myName
		else:
			print(space+styleDef+foreMain+dictionary['No such option!'][language])
			sleep(1)
			clear()
