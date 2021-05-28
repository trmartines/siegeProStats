# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:08:27 2021

@author: tyler
"""
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def student():
   return render_template('../index.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("../result.html",result = result)


if __name__ == 'main':
   app.run(debug = True)
username = request.form.get("username")
password = request.form.get("password")
login = username+':'+password
# Check if any line in the file contains given string
def check_if_string_in_file(file_name, string_to_search):
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False
if(check_if_string_in_file('accounts.csv','tyler9x:builder78!!')):
    file = open("sample.txt","w")
    file.write("admin")
    file.close()
elif(check_if_string_in_file('accounts.csv', login)):
    file.write("user \n",)
else:
    i=1
