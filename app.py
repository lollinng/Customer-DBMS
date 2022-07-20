from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import bcrypt
from flask.wrappers import Request
from db_helper import DBHELPER
import pymongo


app = Flask(__name__)
helper = DBHELPER()
client = pymongo.MongoClient('mongodb://127.0.0.1:27017')
mydb = client['Customer_Database']
user = mydb.customerinformation
admins = mydb.admin_login


@app.route('/admin')
def admin():
    all_data = helper.fetch_all()
    return render_template("index.html", customer=all_data, type='admin')


@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':

        admin_check = request.form.get('mycheckbox')
        if admin_check == 'admin':
            login_admin = admins.find_one({'email': request.form['email']})
            if login_admin:
                if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_admin['password']) == login_admin['password']:
                    session['admin'] = True
                    session['email'] = request.form['email']
                    return redirect(url_for('admin'))
            else:
                flash('You are not admin please untick the box !')
            return render_template("auth.html")

        login_user = user.find_one({'email': request.form['email']})
        if login_user:
            if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['admin'] = False
                session['email'] = request.form['email']
                return redirect(url_for("details", email=session['email']))

        flash('Invalid username/password combination')
    return render_template("auth.html")


@app.route('/product/', methods=['GET', 'POST'])
def product():
    if session['admin'] == True:
        if request.method == 'POST':
            data = helper.get_prod_info1(
                request.form['data'], "products.productname")

            print(data)
            return render_template("product.html", customer=data, type='admin')
        return render_template("product.html", type='admin')
    else:
        return redirect(url_for("details", email=session['email']))


@ app.route('/product_list/', methods=['GET', 'POST'])
def product_list():
    value = request.args.get('button_text')

    data_query = helper.get_prod_info1(value, "products.productname")
    for i in data_query:
        del i['_id']
        for j in i['products']:
            del j['_id']
    print(data_query)
    return jsonify({"data": data_query})


@ app.route('/customer/', methods=['GET', 'POST'])
def customer():
    if session['admin'] == True:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            age = request.form['age']
            gender = request.form['gender']
            numprod = request.form['numprod']

            data = [name, email, phone, age, gender, numprod]
            return redirect(url_for("customer1", data=data))
        return render_template("customer.html", data=0, type='admin')
    else:
        return redirect(url_for("details", email=session['email']))


@ app.route('/customer1/<data>/', methods=['GET', 'POST'])
def customer1(data):
    if request.method == 'POST':
        data = data.strip('][').split(', ')
        for i in range(5):
            data[i] = data[i][1:-1]
        no_products = int(data[5])

        products = []
        for i in range(no_products):
            products.append(helper.get_prod_info(request.form['no'+str(i)]))
        print(products)
        helper.insert_user(data[0], data[1], data[2],
                           data[3], data[4], no_products, products)
        return redirect(url_for("admin"))

    data = data.strip('][').split(', ')
    for i in range(6):
        data[i] = data[i][1:-1]
    data[5] = int(data[5])
    return render_template("customer1.html", data=data, type='admin')


@ app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('sup')
        # if  session.get("USERNAME")
        if session.get('admin') is not None:
            existing_user = admins.find_one({'email': request.form['email']})
            print('admin he is')
        else:
            existing_user = user.find_one({'email': request.form['email']})
            print('not admin')

        if existing_user is None:
            if request.form['pass1'] == request.form['pass2']:
                hashpass = bcrypt.hashpw(
                    request.form['pass1'].encode('utf-8'), bcrypt.gensalt())
                if session.get('admin') is not None:
                    admins.insert_one({
                        'name': request.form['username'],
                        'email': request.form['email'],
                        'phone': request.form['phone'],
                        'password': hashpass
                    })
                    session['email'] = request.form['email']
                    return redirect(url_for('admin'))
                else:
                    user.insert_one({
                        'name': request.form['username'],
                        'email': request.form['email'],
                        'phone': request.form['phone'],
                        'password': hashpass
                    })
                    session['email'] = request.form['email']
                    session['admin'] = False
                    return redirect(url_for('details', email=session['email']))
            else:
                flash("Please type the same password!")
        else:
            flash("That Email id already exists!")
    return render_template("register.html")


@app.route('/update/<email>', methods=['GET', 'POST'])
def update(email):
    data = helper.fetch_user(email, 'email')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        age = request.form['age']
        gender = request.form['gender']
        no_products = int(request.form['prod_no'])
        products = []
        for i in range(no_products):
            products.append(helper.get_prod_info(request.form['no'+str(i)]))
        print(no_products)
        helper.update_user(name, email, phone, age,
                           gender, no_products, products)
        flash("Customer Data Updated Successfully")
        return redirect(url_for('admin'))
    return render_template('update.html', data=data, type='admin')

# @app.route('/add_prod/<email>/', methods = ['GET', 'POST'])
# def add_prod(email):
#     print('hi')
#     data = helper.fetch_user(email,'email')
#     if request.method == 'POST':
#         add = int(request.form['add'])
#         return render_template('update.html',data=data,add=add,type='admin')
#     return render_template('update.html',data=data,type='admin')

# @app.route('/add_prod1/<email>/', methods = ['GET', 'POST'])
# def add_prod1(email):
#     print('hi')
#     data = helper.fetch_user(email,'email')
#     if request.method == 'POST':
#         no_products = 2
#         products = []
#         for i in range(no_products):
#             products.append(helper.get_prod_info(request.form['no'+str(i)]))

#         data['product'] = data['product']+products

#         return render_template('index.html',type='admin')
#     return render_template('update.html',data=data,type='admin')


# This route is for deleting our customer
@app.route('/delete/<email>/', methods=['GET', 'POST'])
def delete(email):
    helper.delete_user(email)
    flash("Customer Data Deleted Successfully")
    return redirect(url_for('admin'))


@app.route('/search/', methods=['GET', 'POST'])
def search():
    if session['admin'] == True:
        if request.method == 'POST':
            value = request.form.getlist('mycheckbox')
            print("this-"+str(value))
            if value == ['1']:
                email = request.form['data']
                print(email)
                data = helper.fetch_user(email, type='email')
                print(data)
            elif value == ['2']:
                name = request.form['data']
                data = helper.fetch_user(name, type='name')
            elif value == ['3']:
                phone = request.form['data']
                data = helper.fetch_user(phone, type='phone')
            elif value == ['4']:
                data = helper.get_prod_info1(
                    request.form['data'], "products.product")
                print(data)
                return render_template("search.html", customer=data, page_type='index', type='admin')
            elif value == ['5']:
                val = int(request.form['val1'])
                data = helper.compare(value=val, operator='gt')
                return render_template("search.html", customer=data, page_type='index', type='admin')
            elif value == ['6']:
                val = int(request.form['val2'])
                data = helper.compare(value=val, operator='lt')
                return render_template("search.html", customer=data, page_type='index', type='admin')
            else:
                return "sorry data not available"
            return render_template("search.html", customer=data, type='admin')
        return render_template("search.html", type='admin')
    else:
        return redirect(url_for("details", email=session['email']))

# This route is for getting the details of the customer


@app.route('/details/<email>/', methods=['GET', 'POST'])
def details(email):
    if session['admin'] == True:
        data = helper.fetch_user(email, type='email')
        return render_template("details.html", customer=data, type='admin')
    else:
        data = helper.fetch_user(email, type='email')
        return render_template("details.html", customer=data, type='admin')


@app.route('/table/<email>/', methods=['GET', 'POST'])
def table(email):
    data = helper.fetch_user(email, type='email')
    return render_template("table.html", customer=data, type='admin')


if __name__ == "__main__":
    app.secret_key = "Secret Key"
    app.run(debug=True)
