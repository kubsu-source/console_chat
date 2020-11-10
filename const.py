from colorama import Fore, Back, Style
from time import sleep
from firebase import firebase
import msvcrt, cursor, colorama

colorama.init()
cursor.hide()

firebase = firebase.FirebaseApplication('https://consolechat-b0ba5.firebaseio.com/', None)

notif_dictionary={
		' left the chat!':[' left the chat!',' покинул(а) чат!'],
		' joined the chat via invitation by ':[' joined the chat via invitation by ',' присоединился(-лась) к чату по приглашению от '],
		' joined the chat!':[' joined the chat!',' присоединился(-лась) к чату!'],
		' created this chat!':[' created this chat!',' создал(а) этот чат!'],
		' created this private chat!':[' created this private chat!',' создал(а) этот закрытый чат!'],
		'SYSTEM':['SYSTEM','СИСТЕМА'],
		}

dictionary={
		'### Concole Chat ###':['### Concole Chat ###','### Консольный Чат ###'],
		'Text message':['Text message','Сообщение'],
		'Invite: ':['Invite: ','Пригласить: '],
		'Loading ...':['Loading ...','Загрузка ...'],
		'This is your name!':['This is your name!','Это Ваше имя!'],
		'User name':['User name','Имя пользователя'],
		'This user is already invited!':['This user is already invited!','Этот пользователь уже приглашен!'],
		'Done!':['Done!','Готово!'],
		'No such user!':['No such user!','Нет такого пользователя!'],
		'### Menu ###':['### Menu ###','### Меню ###'],
		'1) Join chat':['1) Join chat','1) Присоединиться к чату'],
		'2) Create public chat':['2) Create public chat','2) Создать открытый чат'],
		'3) Create private chat':['3) Create private chat','3) Создать закрытый чат'],
		'4) Settings':['4) Settings','4) Настройки'],
		'0) Log out\n':['0) Log out\n','0) Выйти из учетной записи\n'],
		'Your choice: ':['Your choice: ','Ваш выбор: '],
		'No such option!':['No such option!','Такого варианта нет!'],
		'Chat: ':['Chat: ','Чат: '],
		'No such chat!':['No such chat!','Нет такого чата!'],
		'Connecting ...':['Connecting ...','Подключение ...'],
		'Password: ':['Password: ','Пароль: '],
		'You do not have an invitation!':['You do not have an invitation!','У Вас нет приглашения!'],
		'Wrong password!':['Wrong password!','Неверный пароль!'],
		'Name of chat: ':['Name of chat: ','Имя чата: '],
		'Type something!':['Type something!','Напечатайте что-нибудь!'],
		'This name is taken':['This name is taken','Это имя занято'],
		'Password for this chat:':['Password for this chat:','Пароль для этого чата: '],
		'Press tab in the chat to make an invitation for your friend':['Press tab in the chat to make an invitation for your friend','Нажмите Tab в чате, чтобы пригласить Вашего друга'],
		'This way your friend can join this chat by password':['This way your friend can join this chat by password','Таким образом, Ваш друг сможет присоединиться к этому чату с помощью пароля'],
		'Press enter to continue...':['Press enter to continue...','Нажмите enter, чтобы продолжить...'],
		'### Settings ###':['### Settings ###','### Настройки ###'],
		'1) Main Color: ':['1) Main Color: ','1) Главный цвет: '],
		'2) Side Color: ':['2) Side Color: ','2) Побочный цвет: '],
		'3) Brightness: ':['3) Brightness: ','3) Яркость: '],
		'4) Left margin: ':['4) Left margin: ','4) Отступ слева: '],
		'5) Language: ':['5) Language: ','5) Язык: '],
		' space(s)':[' space(s)',' пробел(-ов)'],
		'0) Back':['0) Back','0) Назад'],
		'Input a number!':['Input a number!','Введите число!'],
		'Input a number of spaces: ':['Input a number of spaces: ','Введите число пробелов: '],
		'no level':['no level','нет такого уровня'],
		'error':['error','ошибка'],
		'No Internet!':['No Internet!','Нет доступа к Интернету!'],
		'Login: ':['Login: ','Логин: '],
		'You cannot choose this name!':['You cannot choose this name!','Вы не можете выбрать это имя!'],
		'Email: ':['Email: ','Почта: '],
		'Repeat password: ':['Repeat password: ','Повторите пароль: '],
		'Passwords are not equel!':['Passwords are not equel!','Пароли не совпадают!'],
		'No such account!':['No such account!','Такого аккаунта нет!'],
		'Create new? (y/n): ':['Create new? (y/n): ','Создать новый?(д/н): '],
		'Black':['Black','Черный'],
		'Red':['Red','Красный'],
		'Green':['Green','Зеленый'],
		'Yellow':['Yellow','Желтый'],
		'Blue':['Blue','Синий'],
		'Magenta':['Magenta','Пурпурный'],
		'Cyan':['Cyan','Бирюзовый'],
		'White':['White','Белый'],
		'Dim':['Dim','Тусклый'],
		'Normal':['Normal','Нормальный'],
		'Bright':['Bright','Яркий'],
		'English':['English','English'],
		'Russian':['Русский','Русский'],
		}

COLORS=([Fore.BLACK,'Black'],
		[Fore.RED,'Red'],
		[Fore.GREEN,'Green'],
		[Fore.YELLOW,'Yellow'],
		[Fore.BLUE,'Blue'],
		[Fore.MAGENTA,'Magenta'],
		[Fore.CYAN,'Cyan'],
		[Fore.WHITE,'White'],)

BRIGHTNESS=([Style.DIM,'Dim'],
			[Style.NORMAL,'Normal'],
			[Style.BRIGHT,'Bright'],)

LANGUAGE=('English','Russian')

SYSTEM_NAME='SYSTEM'