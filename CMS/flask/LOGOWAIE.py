from flask import Flask, render_template, request, session, redirect
import sqlite3

from flask import Flask, render_template, request, session, redirect
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'Qwerty123!'

DBASE = "usersRepo"
loginConnector = sqlite3.connect(f'{DBASE}.sqlite', check_same_thread=False)
loginCursor = loginConnector.cursor()

loginCursor.execute(f'''CREATE TABLE IF NOT EXISTS {DBASE}(
        LOGIN VARCHAR(255) PRIMARY KEY,
        PASSWD VARCHAR(255))''')
loginConnector.commit()
loginCursor.close()

loginConnector = sqlite3.connect(f'{DBASE}.sqlite', check_same_thread=False)
loginCursor = loginConnector.cursor()
loginCursor.execute(f'''INSERT OR REPLACE INTO {DBASE} (LOGIN,PASSWD) VALUES ("admin","admin")''')
loginConnector.commit()


class userForm(FlaskForm):
    """Formularz danych logowania"""
    login = StringField('login', validators=[DataRequired()])
    passwd = PasswordField('haslo', validators=[DataRequired()])
    submit = SubmitField('Zatwierdź')


class editForm(FlaskForm):
    """Formularz danych logowania"""
    login = StringField('nowy login', validators=[DataRequired()])
    passwd = PasswordField('nowe hasło', validators=[DataRequired()])
    submit = SubmitField('Zatwierdź')




@app.route('/')
def index():
    form = userForm()
    info = ""
    if 'info' in session:
        info = session['info']
        session.clear()
    print(info)
    return render_template('loginForm.html', headerOne="Zaloguj się.", form=form, action="/loginServiceController",
                           title="logowanie",
                           desc="Podaj dane do logowania", info=info)


@app.route('/register')
def register():
    form = userForm()
    info = ""
    if 'info' in session:
        info = session['info']
        session['info'] = ''
    return render_template('loginForm.html', headerOne="Zarejestruj się.", form=form,
                           action="/registerServiceController",
                           title="rejestrowanie",
                           desc="Podaj nowy login i hasło  użytkownika", info=info)


@app.route('/loginServiceController', methods=["POST"])
def loginServiceController():
    login = request.form['login']
    passwd = request.form['passwd']

    if (login == "admin" and passwd == "admin"):
        session['login'] = login
        session['passwd'] = passwd
        return redirect("/adminInterface")

    loginCursor.execute(f"SELECT * FROM '{DBASE}' WHERE LOGIN = '{login}' AND PASSWD = '{passwd}'")
    sqlRes = loginCursor.fetchall()

    if (len(sqlRes) == 1):
        session['login'] = login
        session['passwd'] = passwd
        return redirect('/userInterface')
    else:
        session['info'] = "Niepoprawny login lub hasło"
        return redirect("/")


@app.route("/adminInterface")
def adminInterface():
    res = loginCursor.execute(f"SELECT * FROM {DBASE} WHERE LOGIN != 'admin'")
    users = res.fetchall()
    info = ''
    if 'info' in session:
        info = session['info']
        session['info'] = ''

    if ('login' in session and 'passwd' in session):
        if (session['login'] == 'admin' and session['passwd'] == 'admin'):
            return render_template("adminInterface.html", headerOne="Zalogowano jako administrator",
                                   desc="Możesz edytować użytkowników", info=info, title="admin", users=users)
    session['info'] = "Brak uprawnień admina"
    return redirect("/")


@app.route("/adminEdit", methods=["POST"])
def adminEdit():
    login = request.form['login']
    passwd = request.form['passwd']
    info = ''
    if 'info' in session:
        info = session['info']
        session['info'] = ''
    session['userInEdit'] = login
    form = editForm()
    return render_template("userInterface.html", headerOne=f"Użytkownik: {login}", form=form,
                           desc="Możesz modyfikować użytkownika", back=True, backAction="/adminInterface",
                           action="/adminUpdateUser")


@app.route("/adminUpdateUser", methods=["GET", "POST"])
def editDataByAdmin():
    login = request.form['login']
    loginOld = session['userInEdit']
    passwd = request.form['passwd']
    try:
        loginCursor.execute(f"SELECT * from '{DBASE}' WHERE LOGIN = '{login}'")
        r = loginCursor.fetchall()
        if (len(r) != 0 and login != loginOld):
            0 / 0
        session['userInEdit'] = login
        session['info'] = "zaaktualizowano pomyślnie dane"
        loginCursor.execute(f"UPDATE {DBASE} SET LOGIN ='{login}', PASSWD = '{passwd}' WHERE LOGIN = '{loginOld}'")
        loginConnector.commit()
        session['info'] = f"Dane użytkownika {login} zaaktualizowano pomyślnie"
    except:
        session['info'] = f"Wystąpił błąd podczas zapisu danych {loginOld}, login {login}  jest zajęty"
    finally:
        return redirect('/adminInterface')


@app.route('/registerServiceController', methods=["POST"])
def registerServiceController():
    login = request.form['login']
    passwd = request.form['passwd']

    try:
        loginCursor.execute(f"SELECT * from '{DBASE}' WHERE LOGIN = '{login}'")
        r = loginCursor.fetchall()
        if (len(r) != 0):
            0 / 0
        loginCursor.execute(f"INSERT INTO '{DBASE}' (LOGIN, PASSWD) VALUES ('{login}', '{passwd}')")
        loginConnector.commit()
        session['info'] = "Utworzono konto"
        session['login'] = login
        session['passwd'] = passwd
        return redirect("/userInterface")
    except:
        session['info'] = "Nie udało się utworzyć użytkownika. Spróbuj zmienić login"
        return redirect("/register")


@app.route("/userInterface", methods=["GET", "POST"])
def UI():
    login = session['login']
    info = ""
    if 'info' in session:
        info = session['info']
        session['info'] = ''
    form = editForm(loginOld=login, login=login)
    return render_template('userInterface.html', headerOne=f"{login} - Zalogowano", form=form, action="/updateUser",
                           title="Zalogowano",
                           desc="Możesz zmienić dane logowania", info=info)


@app.route("/updateUser", methods=["GET", "POST"])
def editData():
    login = request.form['login']
    loginOld = session['login']
    passwd = request.form['passwd']
    try:
        loginCursor.execute(f"SELECT * from '{DBASE}' WHERE LOGIN = '{login}'")
        r = loginCursor.fetchall()
        if (len(r) != 0 and login != loginOld):
            0 / 0
        session['login'] = login
        session['passwd'] = passwd
        session['info'] = "zaaktualizowano pomyślnie dane"
        loginCursor.execute(f"UPDATE {DBASE} SET LOGIN ='{login}', PASSWD = '{passwd}' WHERE LOGIN = '{loginOld}'")
        loginConnector.commit()
    except:
        session['info'] = "Wystąpił błąd, Spróbuj wybrać inny login"
    finally:
        return redirect('/userInterface')


if __name__ == '__main__':
    app.run(debug=True)
