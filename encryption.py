from Cryptodome.Cipher import DES
import ast

from const import *

KEY='12345678'.encode('utf-8')
defKey='12345678'.encode('utf-8')
#KEY'S LEN MUST BE = 8

def pad(text):
	while len(text) % 8 != 0:
		text += b'\x00'

	return text


def encode_str(text,default=False):
	global KEY
	if KEY!=defKey and default==False:
		key=KEY
	else:
		key=defKey
	des = DES.new(key, DES.MODE_ECB)
	text = text.encode('utf-8')
	padded_text = pad(text)
	encrypted_text = des.encrypt(padded_text)
	result=''
	for num in encrypted_text:
		if len(str(num))>3:
			log('len of num > 3')
		while len(str(num))<3:
			num='0'+str(num)
		result+=str(num)
	return result


def decode_str(text,default=False):
	global KEY
	if KEY!=defKey and default==False:
		key=KEY
	else:
		key=defKey
	mas=[]
	temp=text
	while len(temp)>0:
		mas.append(int(temp[:3]))
		temp=temp[3:]
	result=b''
	for num in mas:
		result+=num.to_bytes(1, "little")
	result = ast.literal_eval(str(result))
	des = DES.new(key, DES.MODE_ECB)
	data = des.decrypt(result)
	data=data.replace(b'\x00',b'')
	return str(data.decode('utf-8'))
