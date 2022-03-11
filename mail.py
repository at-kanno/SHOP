import sqlite3, os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import ssl

LOGIN_URL = 'http://www.olivenet.co.jp:6000/'
START_MASSAGE = 'ご注文ありがとうございます。'

MAIN_MESSAGE1 = 'ご注文の内容をご確認ください。'

END_MESSAGE = '\n\n  オリーブネット株式会社\n\n  staff@olivenet.co.jp'

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'

def sendMail(to_name, to_email, order_list, total, tax, amount):

# 送受信先
    cc_email = "at.kanno@icloud.com"
    bcc_email = "atsushi.kanno@nifty.com"
    from_email = "オリーブネット株式会社"
    rcpt = cc_email.split(",") + bcc_email.split(",") + [to_email]

    cset = 'utf-8'
# MIMETextを作成
    if message == '注文':
        message = to_name + '様\n\n' + START_MASSAGE + amount + END_MESSAGE
        subject = "【オリーブネット】ご注文ありがとうございます。"

    msg = MIMEText(message, 'plain', cset)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Cc"] = cc_email

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    sql = 'SELECT MAIL_ADR, PASSWORD FROM USER_TABLE where USER_ID = 2;'
    try:
        c.execute(sql)
        items = c.fetchall()
        n = len(items)
        if n < 1:
            return False
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

    account = items[0][0]
    password = items[0][1]

    servername = "smtp.gmail.com"

# サーバを指定する
    server = smtplib.SMTP_SSL(servername, 465, context=ssl.create_default_context())
    server.set_debuglevel(True)
    if server.has_extn('STARTTLS'):
        server.starttls()

# 認証を行う
    server.login(account, password)
# メールを送信する
    sendToList = to_email.split(',')
    server.sendmail(from_email, rcpt, msg.as_string())
#    server.send_message(msg)
# 閉じる
    return server.quit()
