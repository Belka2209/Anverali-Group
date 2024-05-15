import psycopg2
from fast_bitrix24 import Bitrix
webhook = "https://b24-33c08a.bitrix24.ru/rest/1/9ed1u3ytjdznko0r/"
bx = Bitrix(webhook)

contacts = bx.get_all(
    'crm.contact.list',
    params={
        'select': ['ID', 'NAME']
})

dbname = 'DataBase'
user = 'postgres'
password = '2222'
host = 'localhost'

conn_string = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}'"

try:
    conn = psycopg2.connect(conn_string)
except psycopg2.Error as e:
    print(f"Ошибка при подключении {e}")

cursor = conn.cursor()
cursor.execute('SELECT name FROM names_woman')
all_users_woman = cursor.fetchall()
cursor.execute('SELECT name FROM names_man')
all_users_man = cursor.fetchall()
cursor.close()
conn.close()

for contact in contacts:
    for user in all_users_man:
        if contact['NAME'] == user[0]:
            contact['GENDER'] = 'Мужчина'
            break
        else:
            contact['GENDER'] = None
    if contact['GENDER'] == 'Мужчина':
        continue
    for user in all_users_woman:
        if contact['NAME'] == user[0]:
            contact['GENDER'] = 'Женщина'
            break

# Если нет добавляемого поля, то нужно его добавить, иначе используем имеющееся
# params = {"fields":
# 		{
# 			"FIELD_NAME": "GENDER",
# 			"EDIT_FORM_LABEL": "Пол",
# 			"LIST_COLUMN_LABEL": "Пол",
# 			"USER_TYPE_ID": "string",
# 			"XML_ID": "MY_STRING"
# 		}}
# bx.call('crm.contact.userfield.add', params)

for contact in contacts:
    params = {"ID": contact['ID'],
          "fields":
		{
			"UF_CRM_GENDER": contact['GENDER']
		}}
    bx.call('crm.contact.update', params)
