from ctypes import windll, create_string_buffer
from datetime import datetime
import struct, json

from stuff import *
from encryption import *

foreMain=Fore.WHITE
foreMain_='White'
foreSub=Fore.CYAN
foreSub_='Cyan'
styleDef=Style.BRIGHT
styleDef_='Bright'
#0=eng, 1=rus
language=0
language_='English'
space=''
space_='0'

def get_window_params():
	h = windll.kernel32.GetStdHandle(-12)
	csbi = create_string_buffer(22)
	res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

	if res:
		(bufx, bufy, curx, cury, wattr,
		 left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
		x_win = right - left + 1
		y_win = bottom - top + 1
	else:
		x_win, y_win = 80, 25

	return x_win, y_win, cury, bottom


def get_date():
	now=datetime.now()
	year=str(now.year)
	month=str(now.month)
	day=str(now.day)
	hour=str(now.hour)
	minute=str(now.minute)
	second=str(now.second)

	while len(year)<4:
		year='0'+year
	while len(year)>4:
		year=year[1:]

	while len(month)<2:
		month='0'+month
	while len(day)<2:
		day='0'+day
	while len(hour)<2:
		hour='0'+hour
	while len(minute)<2:
		minute='0'+minute
	while len(second)<2:
		second='0'+second

	return {
	encode_str('year'):encode_str(year),
	encode_str('month'):encode_str(month),
	encode_str('day'):encode_str(day),
	encode_str('hour'):encode_str(hour),
	encode_str('minute'):encode_str(minute),
	encode_str('second'):encode_str(second),
	}


def check_config():
	global foreMain, foreMain_, foreSub, foreSub_, styleDef, styleDef_, space, space_, language, language_
	try:
		f=open('conf.txt','r',encoding='utf-8')
		data=f.read()
		f.close()
		data=data.replace('\n',' ')
		data=json.loads(data)
		foreMain_=data['foreMain']
		foreSub_=data['foreSub']
		styleDef_=data['styleDef']
		language_=data['language']
		space_=data['space']
		get=False
		for i in range(len(COLORS)):
			if foreMain_==COLORS[i][1]:
				foreMain=COLORS[i][0]
				get=True
				break
		if get==False:
			foreMain_='White'

		get=False
		for i in range(len(COLORS)):
			if foreSub_==COLORS[i][1]:
				foreSub=COLORS[i][0]
				get=True
				break
		if get==False:
			foreSub_='Cyan'

		get=False
		for i in range(len(BRIGHTNESS)):
			if styleDef_==BRIGHTNESS[i][1]:
				styleDef=BRIGHTNESS[i][0]
				get=True
				break
		if get==False:
			styleDef_='Bright'

		get=False
		for i in range(len(LANGUAGE)):
			if language_==LANGUAGE[i]:
				language=i
				get=True
				break
		if get==False:
			language_='English'

		try:
			space_=int(space_)
			space=' '*space_
			space_=str(space_)
		except:
			space_='0'
		
	except Exception as e:
		err('0'+str(e))
		data={
		'foreMain' : 'White',
		'foreSub' : 'Cyan',
		'styleDef' : 'Bright',
		'space' : '0',
		'language': 'English'
		}
		
		line='{'
		for i in data.keys():
			line+='"'+i+'"'+str(': ')+'"'+data[i]+'"'+',\n'
		line=line[:-2]
		line+='}'
		f=open('conf.txt','w',encoding='utf-8')
		f.write(line)
		f.close()
	return foreMain, foreMain_, foreSub, foreSub_, styleDef, styleDef_, space, space_, language, language_

check_config()