#print messages when the len of mess is too big
#if len>x ==== if len(mess_text[0])+len(' '+myName+' > ')<=read.window_x:
#shift+letter and shift+special key (page up & etc.) ==== elif key=='shift' or key=='alt' or key=='ctrl':

'''
пользователи ключ=стандартный
	имя шифровать с ключом=имя
		все остальные данные шифр с ключом=хэш пароля

чаты=стандартный
	название публичного чата ключ=стандартный
		сообщения ключ=стандартный
	название приватного чата ключ=стандартный
		сообщения ключ=специальный
		приглашение косят под сообщение ключ=специальный
		в названии приглашения=ключ+имя_нового_участника
'''
from threading import Thread
import win32api, random, string

from auth import *

win32api.SetConsoleTitle(dictionary['### Concole Chat ###'][language])


def id_generator(size=6, chars=string.ascii_uppercase+string.digits+string.ascii_lowercase):
	#mess name
	return ''.join(random.choice(chars) for _ in range(size))


class Sending(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		global to_send, chat_name,windowStop,left_chat
		try:
			while windowStop==False or left_chat==False:
				sleep(1)
				if to_send[0]!='':
					data=to_send[0]
					chats=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
					if to_send[1]==False:
						randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)
						while randMes in chats.keys():
							randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)

						result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+randMes, data)
					else:
						result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+encode_str('users',default=True), data)
					to_send=['',False]
		except Exception as e:
			err('10 '+str(e))


class Window(Thread):
	def __init__(self):
		Thread.__init__(self)


	def run(self):
		global windowStop,left_chat,to_send
		try:
			tx,ty,curl,bottom=get_window_params()
			while windowStop==False or left_chat==False:
				x,y,curl,bottom=get_window_params()
				if tx!=x or ty!=y:
					read.update(mode=1)
					tx,ty=x,y
		except Exception as e:
			err('1'+str(e))


class Writting(Thread):
	def __init__(self):
		Thread.__init__(self)


	def get_mes_keys(self):
		global mess_text, myName, writtingStop, windowStop, readStop,left_chat,chat_type, to_send
		try:
			while writtingStop==False or left_chat==False:
				key = msvcrt.getwch()
				num = ord(key)
				
				if num==27:
					#esc
					text=myName+' left the chat!'
					data={encode_str('name'):encode_str(SYSTEM_NAME),encode_str('text'):encode_str(text),encode_str('time'):get_date()}
					randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)
					chats=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
					while randMes in chats.keys():
						randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)
					result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+randMes, data)
					writtingStop=windowStop=readStop=left_chat=True
					break
				elif num==9:
					#tab
					if chat_type=='private':
						readStop=True
						self.get_invite_keys()
						readStop=False
						read.update(mode=3)
				elif num==224:
					key = msvcrt.getwch()
					num = ord(key)
					if num==71:
						pass
				elif num==8:
					if len(mess_text[0])!=0:
						if mess_text[0][len(mess_text[0])-1]==' ' and mess_text[2]==True:
							mess_text[0]=mess_text[0][:-1]
					mess_text[0]=mess_text[0][:-1]
					mess_text[0]+=' '
					mess_text[2]=True

					temp=start=mess_text[0]
					start=start[:-(len(start)+len(space)+len(' '+myName+' > ')-read.window_x)]
					temp=temp[len(start):]
					if mess_text[1]==1 and len(temp)==1:
						mess_text[1]=0
						read.update(mode=1)
				elif num==13:
					#enter
					temp_mes=mess_text[0]
					print(space+styleDef+foreMain+' '+myName+' > '+foreSub+dictionary['Text message'][language]+' '*(len(temp_mes)-len(dictionary['Text message'][language])),end='\r')
					mess_text=['',0,False]
					#self.send({encode_str('name'):encode_str(myName),encode_str('text'):encode_str(temp_mes),encode_str('time'):get_date()})
					to_send=[{encode_str('name'):encode_str(myName),encode_str('text'):encode_str(temp_mes),encode_str('time'):get_date()},False]
				elif key==' ':
					if len(mess_text[0])!=0:
						if mess_text[0][len(mess_text[0])-1]==' ' and mess_text[2]==True:
							mess_text[0]=mess_text[0][:-1]
							mess_text[2]=False
					mess_text[0]+=' '
				elif key=='shift' or key=='alt' or key=='ctrl':
					pass
				else:
					if len(mess_text[0])!=0:
						if mess_text[0][-1]==' ' and mess_text[2]==True:
							mess_text[0]=mess_text[0][:-1]
							mess_text[2]=False
					mess_text[0]+=key
				

				cursor.hide()
				if len(space)+len(mess_text[0])+len(' '+myName+' > ')<=read.window_x:
					if len(mess_text[0])==0 or (len(mess_text[0])==1 and mess_text[0]==' '):
						print(space+styleDef+foreMain+' '+myName+' > '+foreSub+dictionary['Text message'][language],end='\r')
					elif len(mess_text[0])<len(dictionary['Text message'][language]):
						print(space+styleDef+foreMain+' '+myName+' > '+foreMain+mess_text[0]+(' '*(len(dictionary['Text message'][language])-1)),end='\r')
					else:
						print(space+styleDef+foreMain+' '+myName+' > '+mess_text[0],end='\r')
				else:
					start=mess_text[0]
					start=start[:-(len(start)+len(space)+len(' '+myName+' > ')-read.window_x)]
					if mess_text[1]==0:
						print(space+styleDef+foreMain+' '+myName+' > '+start)
						mess_text[1]=1

					temp=mess_text[0]
					temp=temp[len(start):]
					if len(temp)//read.window_x>mess_text[1]-1:
						middle=temp
						middle=middle[read.window_x*(mess_text[1]):]
						print('',end='\r')
						print(space+styleDef+middle)
						mess_text[1]+=1
					temp=temp[read.window_x*(mess_text[1]-1):]
					print(space+styleDef+temp,end='\r')

		except Exception as e:
			err('3'+str(e))


	def get_invite_keys(self):
		global to_send
		read.update(mode=2)
		address=['',0,False]
		try:
			while writtingStop==False:
				key = msvcrt.getwch()
				num = ord(key)
				
				if num==27:
					#esc
					break
				elif num==9:
					#tab
					pass
				elif num==224:
					key = msvcrt.getwch()
					num = ord(key)
					if num==71:
						pass
				elif num==8:
					if len(address[0])!=0:
						if address[0][len(address[0])-1]==' ' and address[2]==True:
							address[0]=address[0][:-1]
					address[0]=address[0][:-1]
					address[0]+=' '
					address[1]-=1
					address[2]=True
				elif num==13:
					#enter
					temp_mes=address[0]
					print(space+styleDef+foreMain+dictionary['Invite: '][language]+temp_mes)
					print(space+styleDef+foreMain+dictionary['Loading ...'][language])
					if temp_mes==myName:
						address=['',0,False]
						clear()
						print(space+styleDef+foreMain+dictionary['Invite: '][language]+temp_mes)
						print(space+styleDef+foreMain+dictionary['This is your name!'][language])
						sleep(1)
						clear()
						cursor.hide()
						if len(address[0])+len(dictionary['Invite: '][language])<=read.window_x:
							if len(address[0])==0 or (len(address[0])==1 and address[0]==' '):
								print(space+styleDef+foreMain+dictionary['Invite: '][language]+foreSub+dictionary['User name'][language],end='\r')
							elif len(address[0])<len(dictionary['User name'][language]):
								print(space+styleDef+foreMain+dictionary['Invite: '][language]+address[0]+(' '*(len(dictionary['User name'][language])-1)),end='\r')
							else:
								print(space+styleDef+foreMain+dictionary['Invite: '][language]+address[0],end='\r')
						continue
					
					check=firebase.get('/'+encode_str('users',default=True), None)
					find=False
					for i in check.keys():
						if decode_str(i,default=True)==temp_mes:
							find=True
							address=['',0,False]
							try:
								messages=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
								join=decode_str(messages[encode_str('users',default=True)][encode_str(temp_mes,default=True)][1],default=True)
								clear()
								print(space+styleDef+foreMain+dictionary['Invite: '][language]+temp_mes)
								print(space+styleDef+foreMain+dictionary['This user is already invited!'][language])
								sleep(1)
								clear()
							except:
								print(space+styleDef+foreMain+dictionary['Done!'][language])
								sleep(1)
								clear()
								#self.send({encode_str(temp_mes,default=True):[encode_str(myName,default=True),encode_str('False',default=True)]},invite=True)
								to_send=[{encode_str(temp_mes,default=True):[encode_str(myName,default=True),encode_str('False',default=True)]},True]
								break				
					if find==False:
						clear()
						print(space+styleDef+foreMain+dictionary['Invite: '][language]+temp_mes)
						print(space+styleDef+foreMain+dictionary['No such user!'][language])
						address=['',0,False]
						sleep(1)
						clear()


				elif key==' ':
					if len(address[0])!=0:
						if address[0][len(address[0])-1]==' ' and address[2]==True:
							address[0]=address[0][:-1]
							address[2]=False
					address[0]+=' '
				elif key=='shift' or key=='alt' or key=='ctrl':
					pass
				else:
					if len(address[0])!=0:
						if address[0][-1]==' ' and address[2]==True:
							address[0]=address[0][:-1]
							address[2]=False
					address[0]+=key
				
				#if temp!=address[0] and curl-bottom<2:
				cursor.hide()
				if len(space)+len(address[0])+len(dictionary['Invite: '][language])<=read.window_x:
					if len(address[0])==0 or (len(address[0])==1 and address[0]==' '):
						print(space+styleDef+foreMain+dictionary['Invite: '][language]+foreSub+dictionary['User name'][language],end='\r')
					elif len(address[0])<len(dictionary['User name'][language]):
						print(space+styleDef+foreMain+dictionary['Invite: '][language]+address[0]+(' '*(len(dictionary['User name'][language])-1)),end='\r')
					else:
						print(space+styleDef+foreMain+dictionary['Invite: '][language]+address[0],end='\r')
		except Exception as e:
			err('4'+str(e))


class Reading(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.window_x,self.window_y=0,0
		self.conf=None


	def run(self):
		while True:
			try:
				global readStop, messages, chat_name, left_chat
				new=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
				messages=self.sorting(new)
				self.update(mode=1)
				while True:
					while readStop==True or left_chat==True:
						sleep(2)
					while readStop==False and left_chat==False:
						self.window_x,self.window_y,curl,bottom=get_window_params()
						log(str('{} {} {} {}'.format(self.window_x,self.window_y,curl,bottom)))
						new=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
						new=self.sorting(new)
						if new!=messages:
							messages=new
							log('new')
							log(str(curl-bottom))
							if curl-bottom<2 and left_chat==False and readStop==False:
								self.update(mode=1)
						sleep(1)
			except Exception as e:
				err('5'+str(e))

	
	def sorting(self,messages):
		try:
			try:
				temp=messages[encode_str('users',default=True)]
				del messages[encode_str('users',default=True)]
			except:
				pass

			result=[]
			for i in messages.keys():
				result.append('0')
			conf=result.copy()
			times=[]
			for i in messages.keys():
				time=messages[i]
				time=time[encode_str('time')]
				time=int(decode_str(time[encode_str('year')])+decode_str(time[encode_str('month')])+decode_str(time[encode_str('day')])+decode_str(time[encode_str('hour')])+decode_str(time[encode_str('minute')])+decode_str(time[encode_str('second')]))
				times.append(time)
			times.sort()
			today=get_date()
			for i in messages.keys():
				time=messages[i]
				time=time[encode_str('time')]
				num=int(decode_str(time[encode_str('year')])+decode_str(time[encode_str('month')])+decode_str(time[encode_str('day')])+decode_str(time[encode_str('hour')])+decode_str(time[encode_str('minute')])+decode_str(time[encode_str('second')]))
				date_string=decode_str(time[encode_str('day')])+'.'+decode_str(time[encode_str('month')])+'.'+decode_str(time[encode_str('year')])
				conf[times.index(num)]=date_string						

				result[times.index(num)]=messages[i]
			temp=''
			for i in range(len(conf)):
				if conf[i]!=temp:
					temp=conf[i]
				else:
					conf[i]='0'
			self.conf=conf
			return result
		except Exception as e:
			err('6'+str(e))


	def translate(self,message):
		if LANGUAGE[language]=='English':
			return message
		else:
			message=message.copy()
			message[encode_str('name')]=encode_str(notif_dictionary['SYSTEM'][language])
			text=decode_str(message[encode_str('text')])
			for k in notif_dictionary:
				if k in text:
					text=text.replace(k,notif_dictionary[k][language])
					break
			message[encode_str('text')]=encode_str(text)
		return message


	def update(self,mode):
		try:
			global messages, mess_text
			self.window_x,self.window_y,curl,bottom=get_window_params()
			if mode==1:
				cursor.hide()
				clear()
				for i in range(len(messages)):
					if self.conf!=None:
						if self.conf[i]!='0':
							if i > 0:
								if self.conf[i-1]!=self.conf[i]:
									print(space+styleDef+foreMain+'['+self.conf[i]+']')
							else:
								print(space+styleDef+foreMain+'['+self.conf[i]+']')
					if decode_str(messages[i][encode_str('name')])!=SYSTEM_NAME:
						print(space+styleDef+foreMain+'['+decode_str(messages[i][encode_str('time')][encode_str('hour')])+':'+decode_str(messages[i][encode_str('time')][encode_str('minute')])+'] '+decode_str(messages[i][encode_str('name')])+' > '+foreSub+decode_str(messages[i][encode_str('text')]))
					else:
						message=self.translate(messages[i])
						print(space+styleDef+foreMain+'['+decode_str(message[encode_str('time')][encode_str('hour')])+':'+decode_str(message[encode_str('time')][encode_str('minute')])+'] '+foreSub+decode_str(message[encode_str('name')])+' > '+foreSub+decode_str(message[encode_str('text')]))
				temp=0
				for i in range(len(self.conf)):
					if self.conf[i]!='0':
						temp+=1
				for i in range(self.window_y-2-len(messages)-temp):
					print()
				print(space+foreSub+'-'*(self.window_x-len(space)))
				if len(mess_text[0])==0 or (len(mess_text[0])==1 and mess_text[0]==' '):
					print(space+foreMain+' '+myName+' > '+foreSub+dictionary['Text message'][language],end='\r')
				else:
					print(space+foreMain+' '+myName+' > '+foreSub+mess_text[0],end='\r')
			elif mode==2:
				cursor.hide()
				clear()
				print(space+foreMain+dictionary['Invite: '][language]+foreSub+dictionary['User name'][language],end='\r')
			elif mode==3:
				new=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
				new=self.sorting(new)
				cursor.hide()
				clear()
				for i in range(len(messages)):
					if self.conf!=None:
						if self.conf[i]!='0':
							if i > 0:
								if self.conf[i-1]!=self.conf[i]:
									print(space+styleDef+foreMain+'['+self.conf[i]+']')
							else:
								print(space+styleDef+foreMain+'['+self.conf[i]+']')
					if decode_str(messages[i][encode_str('name')])!=SYSTEM_NAME:
						print(space+styleDef+foreMain+'['+decode_str(messages[i][encode_str('time')][encode_str('hour')])+':'+decode_str(messages[i][encode_str('time')][encode_str('minute')])+'] '+decode_str(messages[i][encode_str('name')])+' > '+foreSub+decode_str(messages[i][encode_str('text')]))
					else:
						message=self.translate(messages[i])
						print(space+styleDef+foreMain+'['+decode_str(message[encode_str('time')][encode_str('hour')])+':'+decode_str(message[encode_str('time')][encode_str('minute')])+'] '+foreSub+decode_str(message[encode_str('name')])+' > '+foreSub+decode_str(message[encode_str('text')]))
				for i in range(len(self.conf)-1,-1,-1):
					if self.conf[i]=='0':
						del self.conf[i]
				temp=0
				for i in range(len(self.conf)):
					temp+=1
				for i in range(self.window_y-2-len(messages)-temp):
					print()
				print(space+foreSub+'-'*(self.window_x-len(space)))
				if len(mess_text[0])==0 or (len(mess_text[0])==1 and mess_text[0]==' '):
					print(space+foreMain+' '+myName+' > '+foreSub+dictionary['Text message'][language],end='\r')
				else:
					print(space+foreMain+' '+myName+' > '+foreSub+mess_text[0],end='\r')
		except Exception as e:
			err('7'+str(e)+'; mode: '+str(mode))


def chat():
	global chat_name, messages, mess_text,readStop,windowStop,writtingStop,left_chat,KEY,chat_type

	readStop=windowStop=writtingStop=left_chat=False
	messages=firebase.get('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True), None)
	mess_text=['',0,False]

	if chat_type=='private':
		name=decode_str(messages[encode_str('users',default=True)][encode_str(myName,default=True)][0],default=True)
		join=decode_str(messages[encode_str('users',default=True)][encode_str(myName,default=True)][1],default=True)
		if join=='True':
			text=myName+' joined the chat!'
		else:
			text=myName+' joined the chat via invitation by '+name+'!'
			data={encode_str(myName,default=True):[encode_str(name,default=True),encode_str('True',default=True)]}
			result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+encode_str('users',default=True), data)
	else:
		text=myName+' joined the chat!'

	data={encode_str('name'):encode_str(SYSTEM_NAME),encode_str('text'):encode_str(text),encode_str('time'):get_date()}
	randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)
	while randMes in messages.keys():
		randMes=encode_str(id_generator(random.randint(1,10), string.ascii_uppercase + string.digits),default=True)
	result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+randMes, data)
	readStop=windowStop=writtingStop=False
	return 'menu'


def menu():
	global chat_name, myName, KEY, foreMain, foreMain_,foreSub,foreSub_,space,space_,styleDef,styleDef_,chat_type,language,language_

	mode='main'
	while True:
		clear()
		if mode=='main':
			print(space+styleDef+foreMain+dictionary['### Menu ###'][language])
			print(space+styleDef+foreMain+dictionary['1) Join chat'][language])
			print(space+styleDef+foreMain+dictionary['2) Create public chat'][language])
			print(space+styleDef+foreMain+dictionary['3) Create private chat'][language])
			print(space+styleDef+foreMain+dictionary['4) Settings'][language])
			print(space+styleDef+foreMain+dictionary['0) Log out\n'][language])
			print(space+styleDef+foreMain+dictionary['Your choice: '][language]+foreSub,end='')
			choice=input()
			if choice=='1':
				mode='chat'
			elif choice=='2':
				mode='new'
			elif choice=='3':
				mode='newp'
			elif choice=='4':
				mode='settings'
			elif choice=='0':
				return 'exit'
			else:
				print(space+styleDef+foreMain+dictionary['No such option!'][language])
				sleep(1)
		elif mode=='chat':
			KEY=defKey
			print(space+styleDef+foreMain+dictionary['Chat: '][language]+foreSub,end='')
			chat=input()
			chats=firebase.get('/'+encode_str('chats'), None)
			if chats==None:
				print(space+styleDef+foreMain+dictionary['No such chat!'][language])
				sleep(1)
				return 'menu'
			no_chat=True
			for i in chats.keys():
				if chat == decode_str(i):
					status=decode_str(chats[i][encode_str('info')][encode_str('access')])
					if status=='public':
						KEY=defKey
						print(space+styleDef+foreMain+dictionary['Connecting ...'][language])
						chat_name=chat
						chat_type='public'
						return 'chat'
					else:
						passwd=get_passwd([[dictionary['Chat: '][language],chat]],dictionary['Password: '][language])
						KEY=passwd.encode('utf-8')
						try:
							#this line is here for trying password
							mes=decode_str(chats[i][encode_str('info',default=True)][encode_str('name')])

							chats=firebase.get('/'+encode_str('chats'), None)
							for i in chats.keys():
								if chat == decode_str(i):
									break
							users=chats[i][encode_str('users',default=True)]
							find=False
							for j in users.keys():
								if decode_str(j,default=True)==myName:
									find=True
									break
							if find==False:
								print(space+styleDef+foreMain+dictionary['You do not have an invitation!'][language])
								sleep(2)
								return 'menu'

							print(space+styleDef+foreMain+dictionary['Connecting ...'][language])
							chat_name=chat
							chat_type='private'
							return 'chat'
						except Exception as e:
							err('8'+str(e))
							no_chat=False
							print(space+styleDef+foreMain+dictionary['Wrong password!'][language])
							sleep(1)
							KEY=defKey
							break
			if no_chat==True:
				print(space+styleDef+foreMain+dictionary['No such chat!'][language])
				sleep(1)
				return 'menu'
		elif mode=='new':
			print(space+styleDef+foreMain+dictionary['Name of chat: '][language]+foreSub,end='')
			title=input()
			chats=firebase.get('/'+encode_str('chats'), None)
			if title=='':
				print(space+styleDef+foreMain+dictionary['Type something!'][language])
				sleep(1)
				again=True
			else:
				print(space+styleDef+foreMain+dictionary['Loading ...'][language])
				again=False
				if chats!=None:
					for i in chats.keys():
						if decode_str(i) == title:
							again=True
							print(space+styleDef+foreMain+dictionary['This name is taken'][language])
							sleep(1)
							break
			if again==False:
				KEY=defKey
				chat_name=title
				text=myName+' created this chat!'
				data={encode_str('name'):encode_str(SYSTEM_NAME),encode_str('text'):encode_str(text),encode_str('time'):get_date(),encode_str('access'):encode_str('public')}
				result=firebase.patch('/'+encode_str('chats')+'/'+encode_str(chat_name)+'/'+encode_str('info'), data)
				print(space+styleDef+foreMain+dictionary['Connecting ...'][language])
				chat_type='public'
				return 'chat'
		elif mode=='newp':
			print(space+styleDef+foreMain+dictionary['Name of chat: '][language]+foreSub,end='')
			title=input()
			chats=firebase.get('/'+encode_str('chats'), None)
			if title=='':
				print(space+styleDef+foreMain+dictionary['Type something!'][language])
				sleep(1)
				again=True
			else:
				print(space+styleDef+foreMain+dictionary['Loading ...'][language])
				again=False
				if chats!=None:
					for i in chats.keys():
						if decode_str(i) == title:
							again=True
							print(space+styleDef+foreMain+dictionary['This name is taken'][language])
							sleep(1)
							break
			if again==False:
				KEY=id_generator(size=8)
				print(space+styleDef+foreMain+dictionary['Password for this chat:'][language],KEY)
				KEY=KEY.encode('utf-8')
				print(space+styleDef+foreMain+dictionary['Press tab in the chat to make an invitation for your friend'][language])
				print(space+styleDef+foreMain+dictionary['This way your friend can join this chat by password'][language])
				print(space+styleDef+foreMain+dictionary['Press enter to continue...'][language],end='')
				input()
				chat_name=title
				text=myName+' created this private chat!'
				data={encode_str('name'):encode_str(SYSTEM_NAME),encode_str('text'):encode_str(text),encode_str('time'):get_date(),encode_str('access',default=True):encode_str('private',default=True)}
				result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+encode_str('info',default=True), data)
				data={encode_str(myName,default=True):[encode_str(myName,default=True),encode_str('True',default=True)]}
				result=firebase.patch('/'+encode_str('chats',default=True)+'/'+encode_str(chat_name,default=True)+'/'+encode_str('users',default=True), data)
				print(space+styleDef+foreMain+dictionary['Connecting ...'][language])
				chat_type='private'
				return 'chat'
		elif mode=='settings':
			print(space+styleDef+foreMain+dictionary['### Settings ###'][language])
			print(space+styleDef+foreMain+dictionary['1) Main Color: '][language]+foreSub+dictionary[foreMain_][language])
			print(space+styleDef+foreMain+dictionary['2) Side Color: '][language]+foreSub+dictionary[foreSub_][language])
			print(space+styleDef+foreMain+dictionary['3) Brightness: '][language]+foreSub+dictionary[styleDef_][language])
			print(space+styleDef+foreMain+dictionary['4) Left margin: '][language]+foreSub+space_+dictionary[' space(s)'][language])
			print(space+styleDef+foreMain+dictionary['5) Language: '][language]+foreSub+dictionary[language_][language])
			print(space+styleDef+foreMain+dictionary['0) Back'][language])
			print('\n'+space+styleDef+foreMain+dictionary['Your choice: '][language],end='')
			choice=input()
			if choice=='1':
				for i in range(len(COLORS)):
					print(space+styleDef+foreMain+str(i+1)+') '+COLORS[i][0]+dictionary[COLORS[i][1]][language])
				print()
				print(space+styleDef+foreMain+dictionary['Your choice: '][language],end='')
				col=input()
				try:
					col=int(col)
					if col in range(1,len(COLORS)+1):
						foreMain=COLORS[col-1][0]
						foreMain_=COLORS[col-1][1]
					else:
						print(space+styleDef+foreMain+dictionary['No such option!'][language])
						sleep(1)
				except:
					print(space+styleDef+foreMain+dictionary['Input a number!'][language])
					sleep(1)

			elif choice=='2':
				for i in range(len(COLORS)):
					print(space+styleDef+foreMain+str(i+1)+') '+COLORS[i][0]+dictionary[COLORS[i][1]][language])
				print()
				print(space+styleDef+foreMain+dictionary['Your choice: '][language],end='')
				col=input()
				try:
					col=int(col)
					if col in range(1,len(COLORS)+1):
						foreSub=COLORS[col-1][0]
						foreSub_=COLORS[col-1][1]
					else:
						print(space+styleDef+foreMain+dictionary['No such option!'][language])
						sleep(1)
				except:
					print(space+styleDef+foreMain+dictionary['Input a number!'][language])
					sleep(1)
			elif choice=='3':
				for i in range(len(BRIGHTNESS)):
					print(space+styleDef+foreMain+str(i+1)+') '+BRIGHTNESS[i][0]+dictionary[BRIGHTNESS[i][1]][language])
				print()
				print(space+styleDef+foreMain+dictionary['Your choice: '][language],end='')
				col=input()
				try:
					col=int(col)
					if col in range(1,len(BRIGHTNESS)+1):
						styleDef=BRIGHTNESS[col-1][0]
						styleDef_=BRIGHTNESS[col-1][1]
					else:
						print(space+styleDef+foreMain+dictionary['No such option!'][language])
						sleep(1)
				except:
					print(space+styleDef+foreMain+dictionary['Input a number!'][language])
					sleep(1)
			elif choice=='4':
				print(space+styleDef+foreMain+dictionary['Input a number of spaces: '][language],end='')
				col=input()
				try:
					col=int(col)
					if col<0:
						print(space+styleDef+foreMain+dictionary['Input a number!'][language])
						sleep(1)
					else:
						space_=str(col)
						space=' '*col
				except:
					print(space+styleDef+foreMain+dictionary['Input a number!'][language])
					sleep(1)
			elif choice=='5':
				for i in range(len(LANGUAGE)):
					print(space+styleDef+foreMain+str(i+1)+') '+dictionary[LANGUAGE[i]][language])
				print()
				print(space+styleDef+foreMain+dictionary['Your choice: '][language],end='')
				lang=input()
				try:
					lang=int(lang)
					if lang in range(1,len(LANGUAGE)+1):
						language_=LANGUAGE[lang-1]
						language=lang-1
						win32api.SetConsoleTitle(dictionary['### Concole Chat ###'][language])
					else:
						print(space+styleDef+foreMain+dictionary['No such option!'][language])
						sleep(1)
				except:
					print(space+styleDef+foreMain+dictionary['Input a number!'][language])
					sleep(1)
			elif choice=='0':
				mode='main'
			else:
				print(space+styleDef+foreMain+dictionary['No such option!'][language])
				sleep(1)
			data={
			'foreMain' : foreMain_,
			'foreSub' : foreSub_,
			'styleDef' : styleDef_,
			'space' : space_,
			'language': language_,
			}
			
			line='{'
			for i in data.keys():
				line+='"'+i+'"'+str(': ')+'"'+data[i]+'"'+',\n'
			line=line[:-2]
			line+='}'
			f=open('conf.txt','w',encoding='utf-8')
			f.write(line)
			f.close()


readStop=windowStop=writtingStop=left_chat=False
while True:
	try:
		clear()
		x,y,curl,bottom=get_window_params()
		level='sign_in'
		chat_name=''
		messages=''
		mess_text=['',0,False]
		to_send=['',False]
		myName=''
		chat_type=''
		while True:
			if level=='sign_in':
				KEY=defKey
				level,myName=sign_in()
			elif level=='sign_up':
				KEY=defKey
				level,myName=sign_up()
			elif level=='menu':
				level=menu()
			elif level=='chat':
				readStop=windowStop=writtingStop=left_chat=False
				level=chat()

				sending=Sending()
				sending.start()

				window=Window()
				window.start()

				read=Reading()
				read.start()

				write=Writting()
				write.start()
				write.get_mes_keys()

				del window, read, write
			elif level=='exit':
				clear()
				break
			else:
				print(space+styleDef+foreMain+dictionary['no level'][language])
				input(dictionary['error'][language])
	except Exception as e:
		e=str(e)
		err('9'+str(e))
		if 'HTTPS' in e or 'socket.gaierror' in e or 'TimeoutError' in e:
			readStop=windowStop=writtingStop=False
			clear()
			print(space+styleDef+foreMain+dictionary['No Internet!'][language])
			sleep(1)
