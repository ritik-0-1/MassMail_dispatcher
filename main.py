# importing module
from email.policy import default
from multiprocessing import context
from flask import Flask, render_template, request
import os
import csv
import re
import pandas as pd
import smtplib


app = Flask(__name__)

# reading CSV file
@app.route('/', methods=["GET", "POST"])
def read_file():
    data=[]
    valid_email = []
    invalid_email = []
            
    if request.method == 'POST':
        if request.files:
            # Lists to store valid and invalid emails respectively
            uploaded_file = request.files['filename'] # This line uses the same variable and worked fine
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath) as file:
                data = pd.read_csv("BULKEMAIL.csv")
                # converting column data to list
                email = data['Email Address'].tolist()

                # Regular Expression for validating email
                # Write new regex
                #regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}\b'
                regex = re.compile(r'''(
                [a-zA-Z0-9._%+-]+ # username
                @ # @ symbol 
                [a-zA-Z0-9.-]+ # domain name
                (\.[a-zA-Z]{2,3}) # dot-something
                )''', re.VERBOSE)

                # check email validity and store them in respective lists.
                for i in range(len(email)):
                    if(re.fullmatch(regex, email[i])):
                        valid_email.append(email[i])
                    else:
                        invalid_email.append(email[i])
    global recipients
    recipients = valid_email
    dfvalid = pd.DataFrame((valid_email), columns = ['Valid'])
    dfinvalid = pd.DataFrame((invalid_email), columns = ['InValid'])
    context = {
        "Valid" : dfvalid.values.tolist,
        "InValid" : dfinvalid.values.tolist,
    }
    return render_template("index.html", column_names=dfvalid.columns.values, row_data=list(dfvalid.values.tolist()),zip=zip)
app.config['FILE_UPLOADS']= "E:\\PROJECTS\\internship_proj\\static\\file\\uploads"    

@app.route('/compose', methods=["GET", "POST"])
def compose():
    return render_template('compose.html')

@app.route('/sendmail', methods=["GET", "POST"])
def sendmail():
    recievers = ['hshaheer99@gmail.com','hshaheer99@outlook.com']
    #recievers = recipients
    body = request.form['message']
    for dest in recievers:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("shah19is@cmrit.ac.in", "shah19is@14")
        message = body
        s.sendmail(recievers, dest, message)
        s.quit()
    return render_template('successful.html')

if __name__ == "__main__":
    app.run(debug=True)
    
'''return render_template('index.html', context=context)
    #Sending Mail
    context = {
        "Valid" : dfvalid,
        "InValid" : dfinvalid,
    }
    recievers = valid_email
            for dest in recievers:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("sender_email_id", "sender_email_id_password")
                message = "Message_you_need_to_send"
                s.sendmail("sender_email_id", dest, message)
                s.quit()
'''
    
    #return render_template("index.html", column_names=df1.columns.values, row_data=list(df1.values.tolist()),zip=zip) 

# printing number of valid and invalid emails
#   print("VALID EMAILS: ", len(valid_email))
#   print("INVALID EMAILS: ", len(invalid_email))
# app.config['FILE_UPLOADS']= "/home/shaheer/app/static/file/uploads"
