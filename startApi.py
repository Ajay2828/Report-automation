from flask import Flask, render_template, request
import random
import datetime
import mysql.connector

app = Flask(__name__)



# Function to generate and store a new CAPTCHA
def generate_and_store_captcha():

    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    captcha_text = ''.join(random.choice(characters) for _ in range(6))
    captcha_time = datetime.datetime.now()

    # Connecting to mysql
    myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "Ask20034567A@", database = "demo")  
    mycurr = myconn.cursor()
    
    # query for inserting values
    sql = "insert into captchas(captcha, time) values (%s, %s)"
    val = (captcha_text,captcha_time)

    try:

        mycurr.execute(sql,val)

        #commit the transaction 
        myconn.commit()  

    except mysql.connector.Error as err:
        return err

    mycurr.close()
    myconn.close()

    return captcha_text

@app.route('/')
def render_form():
    captcha = generate_and_store_captcha()
    return render_template('captcha_form.html', captcha = captcha)

@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():

    user_type_time = datetime.datetime.now()
    user_input = request.form.get('captcha')
    captcha_text = request.form.get('captcha_text')

    # Connecting to mysql
    myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "Ask20034567A@", database = "demo")  
    mycurr = myconn.cursor()

    if user_input == captcha_text:

        previous_captcha_time = None

        mycurr.execute("SELECT * from captchas")
        list1 = mycurr.fetchall()

        for i in range(len(list1)):
            if list1[i][0] == captcha_text:
                previous_captcha_time = list1[i][1]

        # Calculating time difference
        time_difference = abs(previous_captcha_time - user_type_time) 
        # Calculate the difference in minutes
        minutes_difference = int(time_difference.total_seconds() / 60)
        print(minutes_difference)
        if minutes_difference < 1.00:
            return "<p>CAPTCHA verification Success!</p>"
        else:
            return "<p>TIME OUT.Invalid!</p>"

    else:
        return "<p>CAPTCHA verification failed!</p>"
    # closing
    myconn.close()
    mycurr.close()
    
if __name__ == '__main__':
    app.run(port=5000)
