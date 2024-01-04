import csv
import pandas as pd
import datetime
import mysql.connector
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 

today = datetime.datetime.today()
print(today.weekday())

# Connecting to mysql
myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "Ask20034567A@", database = "demo")  
mycurr = myconn.cursor()

# mycurr.execute("select * from customer_coupon where coupon_generated_time like '2023-12-%'")
# customer_coupon = mycurr.fetchall()
# mycurr.execute("select * from mobile_details where date like '%-12-2022' and key_id is not null")
# mobile_details = mycurr.fetchall()
mycurr.execute("select * from captchas")
captcha_details = mycurr.fetchall()

# with open('customer_coupon.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(customer_coupon)
# with open('mobile_details.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(mobile_details)
with open('mobile_details.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(captcha_details)

g_login = GoogleAuth()
g_login.LocalWebserverAuth()
drive = GoogleDrive(g_login)
folder = "1bzpzOOPyP08a_1hDVcnf_R6sCNcfnzg1"
import glob, os
os.chdir("/captcha validation")
for file in glob.glob("*.csv"):
    print(file)
    with open(file,"r") as f:
     fn = os.path.basename(f.name)
     file_drive = drive.CreateFile({'parents' : [{'id' : folder}],'title': fn })  
    file_drive.SetContentString(f.read()) 
    file_drive.Upload()
    print("The file: " + fn + " has been uploaded")


