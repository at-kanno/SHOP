import sqlite3, os, hashlib, base64
import random
import string

base_path = os.path.dirname(__file__)
DATA_FILE = base_path + '/venv/data/users.json'
db_path = base_path + '/exam.sqlite'
form_path = base_path + '/templates'

# パスワードからハッシュを生成する
def password_hash(password):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256',
                                 password.encode('utf-8'), salt, 10000)
    return base64.b64encode(salt + digest).decode('ascii')

# パスワードが正しいかを検証する
def password_verify(password, hash):
    b = base64.b64decode(hash)
    salt, digest_v = b[:16], b[16:]
    digest_n = hashlib.pbkdf2_hmac('sha256',
                                   password.encode('utf-8'), salt, 10000)
    return digest_n == digest_v

# 新規ユーザーを追加
def addUser(lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2,\
            company, department, prefecture, city, town, building, status, password, mail_adr):

    hashedPassword = password_hash(password)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'INSERT INTO USER_TABLE (lastname, firstname, lastyomi, firstyomi,'\
          'tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, town,'\
          'building, status, password, mail_adr) VALUES ("'\
           + lastname + '", "' + firstname + '", "' + lastyomi + '", "' + firstyomi + '", "'\
           + str(tel1) + '", "' + str(tel2) + '", "' + str(tel3) + '", "' + str(zip1) + '", "' + str(zip2) + '", "'\
           + company + '", "' + department + '", "' + str(prefecture) + '", "' + city + '", "' + town + '", "'\
           + building + '", ' + str(status) + ', "' + hashedPassword + '", "' + mail_adr + '")'
    try:
        # INSERT
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

# 既存ユーザー情報を更新
def modifyUser(id, lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2,\
            company, department, prefecture, city, town, building, status, password, mail_adr):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET lastname="' + lastname + '", firstname="' + firstname +\
          '", lastyomi="' + lastyomi +'", firstyomi="' + firstyomi + \
          '", tel1="' + tel1 + '", tel2="' + tel2 + '", tel3="' + tel3 +\
          '", zip1="' + zip1 + '", zip2="' + zip2 + '", company="' + company +\
          '", department="' + department + '", prefecture="' + prefecture + \
          '", city="' + city + '", town="' + town + '", building="' + building + \
          '", mail_adr="' + mail_adr + \
          '" where user_id = ' + id
    try:
        # INSERT
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

# ログインできるか確認
def check_login(id, password):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_ID, PASSWORD FROM USER_TABLE WHERE MAIL_ADR = "' + id + '"'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        user_id = items[0][0]
        password2 = items[0][1]
        if password_verify(password, password2):

            conn.close()
            return user_id
        else:
            conn.close()
            return False
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserInfo(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT lastname, firstname, lastyomi, firstyomi, ' \
          'tel1, tel2, tel3, zip1, zip2, company, department, prefecture, city, ' \
          'town, building ,mail_adr ,status ' \
          'FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getStage(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT STAGE FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def setStage(user_id, stage):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET STAGE = ' + str(stage) + \
          ' WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getUserList():

    userlist = []
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT USER_ID, LASTNAME, MAIL_ADR FROM USER_TABLE'
    try:
        c.execute(sql)
        items = c.fetchall()

        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def deleteUser(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'DELETE FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def compareAddrss( address1, address2):
    upper1 = address1.upper()
    upper2 = address2.upper()
    if(upper1 == upper2):
        return True
    else:
        return False

def setPassword(user_id, password):
    hashed_password = password_hash(password)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'UPDATE USER_TABLE SET PASSWORD = "' + hashed_password \
          + '" WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def resetPassword(user_id, old_password, new_password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql1 = 'SELECT PASSWORD FROM USER_TABLE WHERE USER_ID = ' + str(user_id)
    sql2 = 'UPDATE USER_TABLE SET PASSWORD = "' + new_password + '" WHERE USER_ID = ' + str(user_id)
    try:
        c.execute(sql1)
        items = c.fetchall()
        conn.close()
        if items[0][0] != old_password :
            return False
        c.execute(sql2)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getLoginName(id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT MAIL_ADR FROM USER_TABLE where USER_ID = ' + str(id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False


def getLoginPassword(id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT PASSWORD FROM USER_TABLE where USER_ID = ' + str(id)
    try:
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getStatus(user_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT STATUS FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return 0
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getMailadress(user_id):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT LASTNAME, FIRSTNAME, MAIL_ADR FROM USER_TABLE where USER_ID = ' + str(user_id)
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
        conn.close()
        return items
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def makePassword():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(8)))
    # print("Random alphanumeric String is:", result_str)
    return result_str

