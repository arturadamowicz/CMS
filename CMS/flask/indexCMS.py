# from math import floor
import json

from flask import Flask, render_template, request
from flask_bs4 import Bootstrap

# import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Qwerty123!'

boostrap = Bootstrap(app)
links = []

@app.route('/')
def homePage():
    return render_template('homePage.html')

@app.route('/loginTemplate')
def loginTemplate():
    return render_template('loginTemplate.html', label="Login", action="loginCheck")


@app.route('/headerForm')
def headerForm():
    return render_template('headerForm.html')
@app.route('/newsForm')
def newsForm():
    return render_template('newsForm.html')
@app.route('/footerForm')
def footerForm():
    return render_template('footerForm.html')

@app.route('/getLinks')
def getLinks():
    global links
    text = request.args.get("linkText")
    href = request.args.get("linkHref")
    link = [text,href]
    links.append(link)
    return render_template('formResults.html', links=links, action="clearLinks")

@app.route("/clearLinks")
def clearLinks():
    global links
    links=[]
    return render_template('formResults.html', links=links, action="clearLinks")

@app.route('/registerTemplate')
def registerTemplate():
    return render_template('loginTemplate.html', label="Register", action="registerCheck")


#musi byc jakies sprawdzanie czy w bazie, ale nwm jak to zrobic
inBase = True

#jeszcze musi sprawdzic czy admin
@app.route('/loginCheck')
def loginCheck():
    login = request.args.get("login")
    if(inBase):
        if(login == "admin"):
            return render_template('homePage.html')
        return render_template('404.html')
    else:
        return render_template('500.html')

# tu jesli jest to nie dodaje
@app.route('/registerCheck')
def registerCheck():
    if(inBase):
        return render_template('500.html')
    else:
        return render_template('404.html')



@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404

@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)