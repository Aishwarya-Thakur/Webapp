from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import joblib
import random

load_index = 0
global svm_classifier

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def ChangePassword(request):
    if request.method == 'GET':
       return render(request, 'ChangePassword.html', {})

def HomePage(request):
    if request.method == 'GET':
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        status_data = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306, user = 'root', password = 'root', database = 'user',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == user:
                    status_data = row[5]
                    break
            if status_data == 'none':
                status_data = ''   
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+user+'</font></td></tr></table></br></br>'
            output+=getPostData()
            context= {'data':output}
            return render(request, 'UserScreen.html', context)

def ChangeMyPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password', False)
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
                        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'user',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update register set password='"+password+"' where username='"+user+"'"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        status_data = ''
        if db_cursor.rowcount == 1:
            con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'user',charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("select * FROM register")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] == user and row[1] == password:
                        status_data = row[5]
                        break
            if status_data == 'none':
                status_data = ''   
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+user+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+user+'</font></td></tr></table></br></br>'
            output+=getPostData()
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Error in updating status'}
            return render(request, 'UpdateStatus.html', context)      


def EditProfile(request):
    if request.method == 'GET':
        output = ''
        user = ''
        with open("session.txt", "r") as file:
            for line in file:
                user = line.strip('\n')
        output = ''
        username = ''
        password = ''
        contact = ''
        email = ''
        address = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'opinionmining',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register where username='"+user+"'")
            rows = cur.fetchall()
            for row in rows:
                username = row[0]
                password = row[1]
                contact = row[2]
                email = row[3]
                address = row[4]
        output+='<tr><td><b>Username</b></td><td><input type=text name=username style=font-family: Comic Sans MS size=30 value='+name+' readonly></td></tr>'
        output+='<tr><td><b>Password</b></td><td><input type=password name=password style=font-family: Comic Sans MS size=30 value='+password+'></td></tr>'
        output+='<tr><td><b>Contact&nbsp;No</b></td><td><input type=text name=contact style=font-family: Comic Sans MS size=20 value='+contact+'></td></tr>'
        output+='<tr><td><b>Email&nbsp;ID</b></td><td><input type=text name=email style=font-family: Comic Sans MS size=40 value='+email+'></td></tr>'
        output+='<tr><td><b>DOB</b></td><td><input type=text name=dob style=font-family: Comic Sans MS size=60 value='+dob+'></td></tr>'
        context= {'data':output}
        return render(request, 'EditProfile.html', context)    

def Signup(request):
    if request.method == 'POST':
      name = request.POST.get('name', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      dob = request.POST.get('dob', False)


      fs = FileSystemStorage()
      filename = fs.save('C:/Python/WebApp/webapp/static/profiles/'+username+'.png', myfile)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'opinionmining',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(name,password,contact,email,dob) VALUES('"+name+"','"+password+"','"+contact+"','"+email+"','"+dob+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)

def EditMyProfile(request):
    if request.method == 'POST':
      name = request.POST.get('name', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      dob = request.POST.get('dob', False)

      if os.path.exists('C:/Python/WebApp/webapp/static/profiles/'+username+'.png'):
          os.remove('C:/Python/WebApp/webapp/static/profiles/'+username+'.png')

      fs = FileSystemStorage()
      filename = fs.save('C:/Python/WebApp/webapp/static/profiles/'+username+'.png', myfile)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'user',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "update register set name='"+name+"',password='"+password+"',contact='"+contact+"',email='"+email+"',dob='"+dob+"' where username='"+username+"'"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record updated")
      status_data = ''
      if db_cursor.rowcount == 1:
          con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'user',charset='utf8')
          with con:
              cur = con.cursor()
              cur.execute("select * FROM register")
              rows = cur.fetchall()
              for row in rows:
                  if row[0] == username and row[1] == password:
                      status_data = row[5]
                      break
          if status_data == 'none':
              status_data = ''            
          output = ''
          output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+username+'.png width=200 height=200></img></td>'
          output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+username+'</font></td></tr></table></br></br>'
          output+=getPostData()
          context= {'data':output}
          return render(request, 'UserScreen.html', context)
      else:
       context= {'data':'Error in editing profile'}
       return render(request, 'EditProfile.html', context)    
        
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        status_data = ''
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'user',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    status = 'success'
                    status_data = row[5]
                    break
        if status_data == 'none':
            status_data = ''
        if status == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            output = ''
            output+='<table border=0 align=center width=100%><tr><td><img src=/static/profiles/'+username+'.png width=200 height=200></img></td>'
            output+='<td><font size=3 color=black>'+status_data+'</font></td><td><font size=3 color=black>welcome : '+username+'</font></td></tr></table></br></br>'
            output+=getPostData()
            context= {'data':output}
            return render(request, 'UserScreen.html', context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)
