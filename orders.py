import sqlite3, os
import datetime

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'
form_path = base_path + '/templates'

# 新規ユーザーを追加
def saveOrder(user_id, product, quantity, price):

#    now = datetime.datetime.now()
    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now = dt_now.strftime('%Y/%m/%d,%H:%M:%S')

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql1 = 'INSERT INTO ORDER_TABLE (USER_ID'
    sql2 = ""
    sql3 = ', ORDER_DATE ) VALUES (' + str(user_id)
    sql4 = ""
    sql5 = ', "' + str(now) + '")'

    for index, item in enumerate(product):
        if item == "":
            break;
#        if index != 0:
#            sql2 = sql2 + ','
#            sql4 = sql4 + ','
        sql2 = sql2 + ', PRODUCT' + str(index) + ', PRICE' + str(index) + ', AMOUNT' + str(index)
        sql4 = sql4 + ', "' + item + '", ' + str(price[index]) + ', ' + str(quantity[index])

    sql = sql1 + sql2 + sql3 + sql4 + sql5
    try:
        # INSERT
        c.execute(sql)
        conn.commit()
        sql = 'select ORDER_NO from ORDER_TABLE where rowid = last_insert_rowid();'
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        return items[0][0]
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False

def getOrderList (user_id , order_no):

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    sql = 'SELECT * FROM ORDER_TABLE WHERE ORDER_NO = ' + str(order_no)

    orders = [[0] * 3 for i in range(10)]
    try:
        # INSERT
        c.execute(sql)
        items = c.fetchall()
        conn.close()
        order_no = items[0][0]
        user_id = items[0][1]
        for i in range(10):
            if items[0][5+i] is None:
                break;
            orders[i][0] = items[0][5+i]
            orders[i][1] = items[0][25+i]
            orders[i][2] = items[0][15+i]
        return orders
    except sqlite3.Error as e:
        print('sqlite3.Error occurred:', e.args[0])
        conn.close()
        return False
