# flask-is a python framework used to create lightweight web applications
# in python, when creating a flask application
# 1 importy the flask framework
# 2.create a flask application
# 3.create a route
# 4.create a function for the route
from flask import*
import pymysql#for connecting with the database
# create the application
connection = pymysql.connect(host="localhost",user="root",password="",database="drinks_hub")
app=Flask(__name__)
app.secret_key="hgddukjhbkfjmb"
@app.route("/")
def main():
    # client,server,database
    #  server side
    # connection
    connection = pymysql.connect(host="localhost",user="root",password="",database="drinks_hub")
    # create sql query for wines
    sql_wine="select* from drinks where drink_category='wine'"
    # create a the sql query to be executed (for wine)
    # sql for whiskeys
    sql_whiskey='select * from drinks where drink_category="whiskey"'
    # sql for vodkas
    sql_vodka='select * from drinks where drink_category="vodka"'
    # sql for tequilas
    sql_tequila='select * from drinks where drink_category="tequila"'
    # sql for rums
    sql_rum='select * from drinks where drink_category="rum"'
    # sql for gin
    sql_gin='select * from drinks where drink_category="gin"'
    # sql for brandys
    sql_brandy='select * from drinks where drink_category="brandy"'
    # connect
    cursor_wine=connection.cursor()
    # execute the sql query(wines)
    cursor_wine.execute(sql_wine)
    # whiskeys
    cursor_whiskey=connection.cursor()
    # execute the sql query(whiskey)
    cursor_whiskey.execute(sql_whiskey)
    # vodkas
    cursor_vodka=connection.cursor()
    # execute the sql query(vodkas)
    cursor_vodka.execute(sql_vodka)
    # tequilas
    cursor_tequila=connection.cursor()
    # execute the sql query(tequilas)
    cursor_tequila.execute(sql_tequila)
    # rums
    cursor_rum=connection.cursor()
    # execute the sql query(rums)
    cursor_rum.execute(sql_rum)
    # gins
    cursor_gin=connection.cursor()
    # execute the sql query(gins)
    cursor_gin.execute(sql_gin)
    # brandys
    cursor_brandy=connection.cursor()
    # execute the sql query(brandys)
    cursor_brandy.execute(sql_brandy)
    # create a variable to hold the selected products
    wines=cursor_wine.fetchall()
    # whiskeys
    whiskeys=cursor_whiskey.fetchall()
    # vodkas
    vodkas=cursor_vodka.fetchall()
    # tequilas
    tequilas=cursor_tequila.fetchall()
    # rums
    rums=cursor_rum.fetchall()
    # gins
    gins=cursor_gin.fetchall()
    # brandys
    brandys=cursor_brandy.fetchall()
    return render_template("home.html",mywines=wines,mywhiskeys=whiskeys,myvodkas=vodkas,mytequilas=tequilas,myrums=rums,mygins=gins,mybrandys=brandys)

# create a new to display single_item
@app.route("/single_item/<drink_id>")
def single_item(drink_id):
    # connection
    connection = pymysql.connect(host="localhost",user="root",password="",database="drinks_hub")
    # create sql query
    # put the value of drink_id as place holder
    sql_single_item='select * from drinks where drink_id=%s'
    # create cursor
    cursor_single_item=connection.cursor()
    # execute sql query
    cursor_single_item.execute(sql_single_item,(drink_id,))
    # access the variables and save them in a variable
    drink=cursor_single_item.fetchone()
    # create a variable to to hold the fetched product and access it in another page
    # At this Point, we have a product, We can retrieve product category like
    category = drink[4]  # Category is at colm 4

    # We now query to Find Others drinks in this category, We LImit to only 4
    # ADD THIS
    sql2 = "select * from drinks where drink_category = %s LIMIT 4"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, (category,))
    similar = cursor2.fetchall()
    # Now we have similar drinks

    # We now return the drink and similar drinks 
    return render_template('single.html', drink=drink, similar = similar)
# create a route known as sign up
# create an html template called signup.html
# return the sign up.html template in the sign up route
#insert into users(username,email,phone,password)values("Wayne Mukusa","waynemukusa@gmail.com","+254733716561","5002")
@app.route("/signup",methods=['POST','GET'])
def signup():
    # check if there is details posted
    if request.method=='POST':
        # get the details from the user name
        username=request.form['username']
        email=request.form['email']
        phone=request.form['phone']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        connection = pymysql.connect(host="localhost",user="root",password="",database="drinks_hub")
        # validation checks
        if " "in username:
            return render_template("signup.html",error="username must be one word")
        elif "@" not in email:
            return render_template("signup.html",error="Invalid email!!!Email must contain @")
        elif not phone.startswith ("+254"):
            return render_template("signup.html",error="Phone number must start with with +254")
        elif password !=confirm_password:
            return render_template("signup.html",error="Password does not match, confirm password")
        elif len(password) < 8:
            return render_template("signup.html",error="Password must have 8 characters or more")
        else:
            sql='insert into users(username,email,phone,password)values(%s,%s,%s,%s)'
            # create a cursor to execute the sql
            cursor=connection.cursor()
            # execute the sql
            cursor.execute(sql,(username,email,phone,password))
            # commit the records to the database
            connection.commit()
        return render_template('signup.html',success="Registration successful")
    else:
        return render_template('signup.html',message="Please enter your details to sign up!!!")
@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql="select * from users where username=%s and password=%s"
        # create cursor
        cursor=connection.cursor()
        # execute the query
        cursor.execute(sql,(username,password))
        # check if there ias auser with the above details
        if cursor.rowcount==0: #theare is no user saved with the above details
            return render_template('signin.html',error='Invalid Login details. Try again')
        else:
            session['key']=username
            return redirect('/') #redirect to home page 
    else:
        return render_template('signin.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/signin')
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesa', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/" class="btn btn-dark btn-sm">Back to Products</a>'
@app.route('/dealers', methods=['POST', 'GET'])
def dealers():
    if request.method == 'POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        town=request.form['town']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        phone=request.form['phone']
        connection = pymysql.connect(host="localhost",user="root",password="",database="drinks_hub")
        # validation checks
        if " "in firstname:
            return render_template("dealers.html",error="Firstname must be one word")
        elif " "in lastname:
            return render_template("dealers.html",error="Lastname must be one word")
        elif " "in town:
            return render_template("dealers.html",error="Town should not be left blank.Enter town name!")
        elif password !=confirm_password:
            return render_template("dealers.html",error="Password does not match, confirm password")
        elif len(password) < 8:
            return render_template("dealers.html",error="Password must have 8 characters or more")
        elif not phone.startswith ("+254"):
            return render_template("dealers.html",error="Phone number must start with with +254")
        else:
            sql='insert into dealers(firstname,lastname,town,password,phone)values(%s,%s,%s,%s,%s)'
            # create a cursor to execute the sql
            cursor=connection.cursor()
            # execute the sql
            cursor.execute(sql,(firstname,lastname,town,password,phone))
            # commit the records to the database
            connection.commit()
        return render_template('dealers.html',success="Registration was successful")
    else:
        return render_template('dealers.html',message="Please enter your details to sign up!!!")
        
app.run(debug=True)

