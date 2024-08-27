from flask import Flask 
from flask import url_for
from flask import redirect
from flask import request 
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('login.html')

@app.route("/invoices")
def invoices():
    return render_template('invoice.html')

@app.route("/payment")
def payment():
    return render_template('payment.html')

@app.route("/greeting/<name>")
def gretting(name):
     return f"""
<html>
<head>
 
    <title>Hello World</title>
</head>
<body>
    <h1> Hello {name}, </h1>
     <a href="/Products">Products</a>
</body>
</html>
"""
@app.route("/simpleinterest/<int:principal>/<int:period>")
@app.route("/simpleinterest/<int:principal>")
@app.route("/simpleinterest/<int:period>", defaults={'principal': 1000, 'rate': 60})
@app.route("/simpleinterest/<int:principal>/<int:period>", defaults={'rate': 60})
@app.route("/simpleinterest/<int:principal>", defaults={'period': 1, 'rate': 60})
def simpleInterest(princple,period,rate):
    interest =(princple*period*rate/100)
             
             
    return f"""
<html >
<head>
 
    <title>Hello World</title>
</head>
<body>
  <table>
        <tr>
            <td>Princple</td>
            <td>{princple}</td>
        </tr>
        <tr>
        <td>Rate</td>
            <td>{rate}</td>

        </tr>
        <tr>
        <td>Period</td>
            <td>{period}</td>

        </tr>
        <tr>
            <td>Interest Amount:</td>
            <td>{interest}</td>
        </tr>
        <tr>
            <td>Total Amount to be paid:</td>
            <td>{interest + int(princple)}</td>
        </tr>
    </table>

 </body>
 </html>
 """
@app.route("/demoredirect")
def demoredirect():
     return redirect(url_for('greeting',name='Peter'))
 
@app.post("/login")
def login():
     return """
 <html>
    <head><title></title></head>
    <body>
    
     <form action="/verifylogin">
        <input type="text" name="emailaddress" id="emailaddress"/>
        <input type="password" name="password" id="password"/>
        <input type="submit" name="submitbtn" id="Login"/>
    </form>
    
    </body>
   
</html>
 
 """
@app.route('/verifylogin')
def verifylogin():
    
   emailadress= request.form['emailadress']
   password=request.form['password']
   if emailadress == "admin@gmail.com" and password == "pwd123":
      return f""" 
 
<html>
    <head><title>Verify Login</title></head>
    <body>
        <h1> Verify Login </h1>
        <h6>{request.form['emailadress']}</h6>
        <h6>{request.form['password']}</h6>
        
    </body>
</html>

 
 """
   else :
     return 
     redirect(url_for('login'))
     
     
     
@app.route("/goodlogin")
def goodLokingLogin():
    return render_template('login.html')    