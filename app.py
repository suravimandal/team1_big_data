from flask import Flask, flash, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlite3 import Error
import pandas as pd
from os import listdir
import os
from os.path import isfile, join



from datetime import datetime
import csv
import psycopg2
app = Flask(__name__)

if app.config['ENV'] == 'development':
    app.config.from_object('config.DevelopmentConfig')
else:
    app.config.from_object('config.ProductionConfig')
conn = psycopg2.connect(host=app.config['DB_HOST'], dbname=app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASS'])
cur = conn.cursor()


ALLOWED_EXTENSIONS = {'txt','csv'}
app.config['']=''

def int_checker(lst):
    x = True
    for n in lst:
        if isinstance(str(n), int) is False:
            if x is True and str(n).isdigit() is False:  
                x = False
        elif x is True:
            x=True    
    return x
def table_creation_script(file_name, tableName):
    my_csv = pd.read_csv(file_name)
  
    with open(file_name, 'r') as f:
        i = next(f) # Skip the header row.
        parameterList = i.split(',')
        for i,parameter in enumerate(parameterList):
            if int_checker(parameter[0]):
                parameterList[i] = 's'+parameter
                    
        #print(len(parameterList))ser_account
        reader = csv.reader(f)
        for row in reader:
            ExampleRowList = row
    strq ="""CREATE TABLE IF NOT EXISTS """ + tableName+"""
        (
            """
    i = 0
    for parameter in parameterList:
        #print(i)
        if int_checker(my_csv.iloc[:, i].values):
            if parameter == 'Id':
                strq = strq + parameter + """ INTEGER NOT NULL PRIMARY KEY"""
            else:
                strq=strq+parameter+ """ INTEGER"""
        else:
            if len(ExampleRowList[i].split('.'))==2:
                strq=strq+parameter+""" DECIMAL"""
            else:
                strq=strq+parameter+""" TEXT"""
      
        if i!=len(parameterList)-1:
            strq=strq+""",
            """
        
        else:
            
            strq=strq+"""
            );"""
        i=i+1
    #print(strq)
    return strq
# sql_file = open('V1__init.sql','r')
# def copy_last_row(fileName):
#     with open(fileName, 'r') as f:
#         i= next(f) # Skip the header row.
#         reader = csv.reader(f)

#         for row in reader:
#             l = row
#         return l

def upload_csv_to_database(file_name):
    with open(file_name, 'r') as f:
        i = next(f)
        table_name = ''
        for p in i.split(','):
            table_name = table_name + p
        
        try:
            strq = table_creation_script(file_name, table_name)
            print(strq)
            cur.execute( strq)
            
            try:
                cur.copy_from(f, table_name, sep=',')
                conn.commit()
            except DatabaseError:
                transaction.rollback()
                print("data already exists in the database")
           

        except DatabaseError:
            transaction.rollback()
            print("table already exists")
        




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

print(os.getcwd() + '/UPLOADS/')
	
@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            
            filename = secure_filename(file.filename)
            
            file.save(os.path.join(os.getcwd() + '/UPLOADS', filename))
        return redirect('/')  
   else:
        #onlyfiles = [f for f in listdir(os.path.join(app.config['UPLOAD_FOLDER'])) if isfile(join('', f))]
        onlyfiles = listdir(os.getcwd() + '/UPLOADS/')
        
        return render_template('index.html', files=onlyfiles)

@app.route('/delete/file/<string:filename>')
def delete(filename):
    
    try:
        os.remove( os.getcwd() + '/UPLOADS/' + filename)
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
@app.route('/delete/database/<string:filename>')
def delete_database(filename):
    with open('UPLOADS/' + filename, 'r') as f:
        i = next(f)
        table_name = ''
        for p in i.split(','):
            if len(table_name)<63:
                table_name = table_name + p
            else:
                break
    try:
        print(table_name)
        cur.execute("TRUNCATE "+ table_name)
        return redirect('/')
    except:
        transaction.rollback()
        return 'There was a problem deleting that task'
@app.route('/insert/<string:filename>')
def insert(filename):
    try:
        upload_csv_to_database('UPLOADS/'+filename)
        return redirect('/')
    except :
        transaction.rollback()

@app.route('/getData/<string:filename>', methods=['GET']) 
def contextget(filename):
    with open('UPLOADS/'+filename, 'r') as f:
        i = next(f)
        table_name = ''
        for p in i.split(','):
            table_name = table_name + p
    sql_query ="""SELECT * FROM """ + table_name
    try:
        out = cur.execute(sql_query)
        context_records = cur.fetchall() 
        conn.commit()
        return render_template('index.html', records=context_records, column_names = i.split(','))
    except:
        transaction.rollback()


if __name__ == "__main__":
    
    app.run()