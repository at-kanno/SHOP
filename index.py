# index.py
from flask import Flask, session, render_template, request, redirect, url_for
import sqlite3, os
from users import makePassword, addUser, modifyUser,check_login
from mail import sendMail
from orders import saveOrder, getOrderList

app = Flask(__name__)
app.secret_key = "cairocoders-ednalan"

base_path = os.path.dirname(__file__)
db_path = base_path + '/exam.sqlite'

prefec = ["都道府県",
          "北海道",
          "青森県",
          "岩手県",
          "秋田県",
          "山形県",
          "宮城県",
          "福島県",
          "茨城県",
          "栃木県",
          "群馬県",
          "埼玉県",
          "千葉県",
          "東京都",
          "神奈川県",
          "新潟県",
          "富山県",
          "石川県",
          "福井県",
          "山梨県",
          "長野県",
          "岐阜県",
          "静岡県",
          "愛知県",
          "三重県",
          "滋賀県",
          "京都府",
          "大阪府",
          "兵庫県",
          "奈良県",
          "和歌山県",
          "鳥取県",
          "島根県",
          "岡山県",
          "広島県",
          "山口県",
          "徳島県",
          "香川県",
          "愛媛県",
          "高知県",
          "福岡県",
          "佐賀県",
          "長崎県",
          "熊本県",
          "大分県",
          "宮崎県",
          "鹿児島県",
          "沖縄県", ]


@app.route('/')
def products():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        return render_template('products.html', products=rows)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/add', methods=['POST'])
def add_product_to_cart():

    cursor = None
    try:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']
        _next = request.form['next']

        # validate the received values
        if _quantity and _code and request.method == 'POST':
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE code= "' + _code + '"')
            row = cursor.fetchone()

            itemArray = {
                row[1]: {'name': row[2], 'code': row[1], 'quantity': _quantity, 'price': row[5],
                          'image': row[3], 'total_price': _quantity * row[5]}}

#                row['code']: {'name': row['name'], 'code': row['code'], 'quantity': _quantity, 'price': row['price'],
#                              'image': row['image'], 'total_price': _quantity * row['price']}}

            all_total_price = 0
            all_total_quantity = 0

            session.modified = True
            if 'cart_item' in session:
                if row[1] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        if row[1] == key:
                            old_quantity = session['cart_item'][key]['quantity']
                            total_quantity = old_quantity + _quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row[5]
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = int(session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
                    tax = int(all_total_price * 0.1)
                    amount = int(all_total_price + tax)
            else:
                session['cart_item'] = itemArray
                all_total_quantity = all_total_quantity + _quantity
                all_total_price = int(all_total_price + _quantity * row[5])
                tax = int(all_total_price * 0.1)
                amount = int(all_total_price + tax)

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            session['tax'] = tax
            session['amount'] = amount

        if _next == 'カートに入れる':
            return redirect(url_for('.products'))
        else:
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


@app.route('/delete/<string:code>')
def delete_product(code):
    try:
        all_total_price = 0
        all_total_quantity = 0
        session.modified = True

        for item in session['cart_item'].items():
            if item[0] == code:
                session['cart_item'].pop(item[0], None)
                if 'cart_item' in session:
                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = int(session['cart_item'][key]['total_price'])
                        all_total_quantity = all_total_quantity + individual_quantity
                        all_total_price = all_total_price + individual_price
                        tax = int(all_total_price * 0.1)
                        amount = int(all_total_price + tax)
                break

        if all_total_quantity == 0:
            session.clear()
        else:
            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            session['tax'] = tax
            session['amount'] = amount

        return redirect(url_for('.products'))
    except Exception as e:
        print(e)


def array_merge(first_array, second_array):
    if isinstance(first_array, list) and isinstance(second_array, list):
        return first_array + second_array
    elif isinstance(first_array, dict) and isinstance(second_array, dict):
        return dict(list(first_array.items()) + list(second_array.items()))
    elif isinstance(first_array, set) and isinstance(second_array, set):
        return first_array.union(second_array)
    return False


@app.route('/procedure')
def procedure():
    return render_template('login.html',
                           )
# ユーザー認証
@app.route('/login', methods=['POST'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    if id == '':
        return '<h3>失敗:IDが空です。</h3>'
    # パスワードを照合
    user_id = check_login(id, pw)
    if user_id == False:
        return '<h3>パスワードが一致しません。</h3>'
    session['login'] = id
    return render_template('main-menu.html',
                               user_id=user_id,
                               status=status,
                               )

# ログインしているか調べる
@app.route('/is_login')
def is_login():
    if 'login' in session:
        return "on"
    else:
        return "off"
    return 'login' in session



# ログアウト処理
@app.route('/logout', methods=['POST'])
def logout():
    user_id = int(request.form['user_id'])
    setStage(user_id, 0)
    return render_template(
        'login.html',
        )

@app.route('/registration', methods=['POST'])
def registration():
    user_id = int(request.form['user_id'])

    product = [''] * 10
    quantity = [0] * 10
    price = [0] * 10
#    product = ''
#    quantity = 0
#    price = 0
    all_total_quantity = 0
    all_total_price = 0
    index = 0

    for key, value in session['cart_item'].items():
        individual_quantity = int(session['cart_item'][key]['quantity'])
        individual_price = int(session['cart_item'][key]['total_price'])
        product[index] = session['cart_item'][key]['name']
        quantity[index] = int(session['cart_item'][key]['quantity'])
        price[index] = int(session['cart_item'][key]['total_price'])
        all_total_quantity = all_total_quantity + individual_quantity
        all_total_price = all_total_price + individual_price
        tax = int(all_total_price * 0.1)
        amount = int(all_total_price + tax)
        index += 1

    order_no = saveOrder(user_id, product, quantity, price);

    lastname = request.form.get('lastname')
    if lastname is None:
        lastname = ''
    firstname = request.form.get('firstname')
    if firstname is None:
        firstname = ''
    lastyomi = request.form.get('lastyomi')
    if lastyomi is None:
        lastyomi = ''
    firstyomi = request.form.get('firstyomi')
    if firstyomi is None:
        firstyomi = ''
    tel1 = request.form.get('tel1')
    if tel1 is None:
        tel1 = ''
    tel2 = request.form.get('tel2')
    if tel2 is None:
        tel2 = ''
    tel3 = request.form.get('tel3')
    if tel3 is None:
        tel3 = ''
    telno = ''
    if tel1 == '' and tel2 == '' and tel3 == '':
        telno = ''
    elif tel1 != '' and tel2 != '' and tel3 != '':
        telno = tel1 + '-' + tel2 + '-' + tel3
    elif tel2 == '' and tel3 == '':
        telno = tel1
    elif tel1 == '' and tel3 == '':
        telno = tel2
    elif tel1 == '' and tel2 == '':
        telno = tel3
    elif tel3 == '':
        telno = tel1 +  '-' + tel2
    elif tel2 == '':
        telno = tel1 +  '-' + tel3
    else:
        telno = tel2 +  '-' + tel3
    company = request.form.get('company')
    if company is None:
        company = ''
    department = request.form.get('department')
    if department is None:
        department = ''
    zip1 = request.form.get('zip1')
    if zip1 is None:
        zip1 = ''
    zip2 = request.form.get('zip2')
    if zip2 is None:
        zip2  = ''
    zipno = ''
    if zip1 == '' and zip2 == '':
        zipno = ''
    elif zip1 != '' and zip2 != '':
        zipno = zip1 + '-' + zip2
    elif tel2 == '':
        zipno = zip1
    else:
        zipno = tel2
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    if city is None:
        city = ''
    town = request.form.get('town')
    if town is None:
        town = ''
    building = request.form.get('building')
    if building is None:
        building = ''
    mail_adr = request.form.get('mail_adr')
    if mail_adr is None:
        mail_adr = ''
    retype = request.form.get('retype')
    if retype is None:
        retype = ''
    error_no = 0

    return render_template('register.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           telno=telno,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           zipno=zipno,
                           prefecture=prefecture,
                           prefec=prefec,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           error_no=error_no,
                           order_no=order_no,
                           )


@app.route('/confirmation', methods=['POST'])
def confirmation():
    user_id = int(request.form.get('user_id'))
    order_no = int(request.form.get('order_no'))
    command = request.form.get('command')

#    error_no = int(request.form.get('error_no'))
    error_no = 0

    if command == 'modify':
        id = int(request.form.get('id'))
    else:
        id = 0
    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    telno = ''
    if tel1 == '' and tel2 == '' and tel3 == '':
        telno = ''
    elif tel1 != '' and tel2 != '' and tel3 != '':
        telno = tel1 + '-' + tel2 + '-' + tel3
    elif tel2 == '' and tel3 == '':
        telno = tel1
    elif tel1 == '' and tel3 == '':
        telno = tel2
    elif tel1 == '' and tel2 == '':
        telno = tel3
    elif tel3 == '':
        telno = tel1 +  '-' + tel2
    elif tel2 == '':
        telno = tel1 +  '-' + tel3
    else:
        telno = tel2 +  '-' + tel3
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    zipno = ''
    if zip1 == '' and zip2 == '':
        zipno = ''
    elif zip1 != '' and zip2 != '':
        zipno = zip1 + '-' + zip2
    elif tel2 == '':
        zipno = zip1
    else:
        zipno = tel2
    prefecture = request.form.get('prefecture')
    if prefecture == '都道府県':
        prefecture = ''
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    member =request.form.get('member')
    if member == 'on':
        ap = 'Checked'
    else:
        ap = ''

    if firstname == "" or lastname == "":
        error_no = 11
    if mail_adr == "" or retype == "":
        error_no = 12
    if mail_adr != retype:
        error_no = 1

    if error_no != 0:
        # エラー処理
        if prefecture != "":
            try:
                pref = prefec.index(prefecture)
            except:
                pref = 0
        if id == 0:
            return render_template('register.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   telno=telno,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   zipno=zipno,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref = pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   error_no=error_no,
                                   order_no=order_no,
                                   )


        else:
            return render_template('modification.html',
                                   lastname=lastname,
                                   firstname=firstname,
                                   lastyomi=lastyomi,
                                   firstyomi=firstyomi,
                                   tel1=tel1,
                                   tel2=tel2,
                                   tel3=tel3,
                                   telno=telno,
                                   company=company,
                                   department=department,
                                   zip1=zip1,
                                   zip2=zip2,
                                   zipno=zipno,
                                   prefecture=prefecture,
                                   prefec=prefec,
                                   pref=pref,
                                   city=city,
                                   town=town,
                                   building=building,
                                   mail_adr=mail_adr,
                                   retype=retype,
                                   user_id=user_id,
                                   id=id,
                                   error_no=error_no,
                                   )

    order_list = [0 for i in range(100)]
    order_list = getOrderList(user_id, order_no)

    total = 0
    for i in range(len(order_list)):
        if order_list[i][0] == 0:
            break
        total = total + int(order_list[i][2])
    tax = int(total * 0.1)
    amount = total + tax

    return render_template('confirm.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           telno=telno,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           zipno=zipno,
                           prefecture=prefecture,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           autoPassword=ap,
                           user_id=user_id,
                           id=id,
                           order_no=order_no,
                           order_list=order_list,
                           total=total,
                           tax=tax,
                           total_amount=amount,
                           )


@app.route('/modification', methods=['POST'])
def modification():
    user_id = int(request.form['user_id'])
    id = int(request.form['id'])
    error_no = request.form['error_no']

    lastname = request.form.get('lastname')
    firstname = request.form.get('firstname')
    lastyomi = request.form.get('lastyomi')
    firstyomi = request.form.get('firstyomi')
    tel1 = request.form.get('tel1')
    tel2 = request.form.get('tel2')
    tel3 = request.form.get('tel3')
    telno = request.form.get('telno')
    company = request.form.get('company')
    department = request.form.get('department')
    zip1 = request.form.get('zip1')
    zip2 = request.form.get('zip2')
    zipno = request.form.get('zipno')
    prefecture = request.form.get('prefecture')
    city = request.form.get('city')
    town = request.form.get('town')
    building = request.form.get('building')
    mail_adr = request.form.get('mail_adr')
    retype = request.form.get('retype')

    if prefecture != "":
        try:
            pref = prefec.index(prefecture)
        except:
            pref = 0

    return render_template('modification.html',
                           lastname=lastname,
                           firstname=firstname,
                           lastyomi=lastyomi,
                           firstyomi=firstyomi,
                           tel1=tel1,
                           tel2=tel2,
                           tel3=tel3,
                           telno=telno,
                           company=company,
                           department=department,
                           zip1=zip1,
                           zip2=zip2,
                           zipno=zipno,
                           prefecture=prefecture,
                           prefec=prefec,
                           pref=pref,
                           city=city,
                           town=town,
                           building=building,
                           mail_adr=mail_adr,
                           retype=retype,
                           user_id=user_id,
                           id=id,
                           error_no=error_no,
                           )


@app.route('/updateX', methods=['GET', 'POST'])
def updateX():
    user_id = request.form.get("user_id", "")
    id = request.form.get("id", "")
    if id == "":
        id = 0

    lastname = request.form.get("lastname", "")
    firstname = request.form.get("firstname", "")
    lastyomi = request.form.get("lastyomi", "")
    firstyomi = request.form.get("firstyomi", "")
    tel1 = request.form.get("tel1", "")
    tel2 = request.form.get("tel2", "")
    tel3 = request.form.get("tel3", "")
    tel3 = request.form.get("telno", "")
    zip1 = request.form.get("zip1", "")
    zip2 = request.form.get("zip2", "")
    zip2 = request.form.get("zipno", "")
    company = request.form.get("company", "")
    department = request.form.get("department", "")
    pref = request.form.get("pref", "")
    prefecture = request.form.get("prefecture", "")
    city = request.form.get("city", "")
    town = request.form.get("town", "")
    building = request.form.get("building", "")
    mail_adr = request.form.get("mail_adr", "")

    member = request.form.get('member')
    if member == 'on' or member == 'Checked':
        mflag = True
    else:
        mflag = False

    status = 0

    password = ""

    try:
        if id == 0 or id == '0':
            addUser(lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                    company, department, prefecture, city, town, building, status, password, mail_adr)
        else:
            modifyUser(id, lastname, firstname, lastyomi, firstyomi, tel1, tel2, tel3, zip1, zip2, \
                       company, department, prefecture, city, town, building, status, password, mail_adr)
    except:
        return render_template('error2.html',
                               user_id=user_id,
                               error_message='失敗しました。',
                               )
    if member == 'on' or member == 'Checked':
        sendMail(lastname + firstname, mail_adr, password)
    return render_template('success.html',
                           user_id=user_id,
                           message='成功しました。',
                           )

if __name__ == "__main__":
    app.run(debug=True)