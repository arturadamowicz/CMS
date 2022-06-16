import sqlite3

import flask_cors
from flask import Flask, render_template, request, session, redirect
from flask import Response
from flask_bs4 import Bootstrap
from flask_wtf import FlaskForm
from wtforms import Form, RadioField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


def open_binary_local_file(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def save_file_to_repo(name, file_type, binary_file):
    connection = sqlite3.Connection("CMS_REPO.sqlite")
    cursor = connection.cursor()
    sqlite_insert_blob_query = """ INSERT INTO FILES (name, type, file) VALUES (?, ?, ?)"""
    cursor.execute(sqlite_insert_blob_query, (name, file_type, binary_file))
    connection.commit()
    connection.close()


def update_file_in_repo(name, file_type, binary_file):
    connection = sqlite3.Connection("CMS_REPO.sqlite")
    cursor = connection.cursor()
    sqlite_insert_blob_query = """UPDATE FILES SET file=? WHERE name=?"""
    cursor.execute(sqlite_insert_blob_query, (binary_file, name))
    connection.commit()
    connection.close()


def repo_init():
    connection = sqlite3.Connection("CMS_REPO.sqlite")
    cursor = connection.cursor()

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS FILES (name TEXT PRIMARY KEY, type TEXT, file BLOB)""")
    connection.commit()

    cursor.execute("""SELECT count(*) FROM FILES WHERE name='data.json'""")
    response = cursor.fetchall()
    if response[0][0] == 0:
        save_file_to_repo("data.json", "json", open_binary_local_file("baseWebsite/data.json"))
        save_file_to_repo("logo.png", "png", open_binary_local_file(f"baseWebsite/gfx/logo2.png"))
        for i in range(5):
            save_file_to_repo(f"slider/photo-{i + 1}.jpg", "jpg",
                              open_binary_local_file(f"baseWebsite/gfx/slider/photo-{i + 1}.jpg"))
        print("Dodano pliki do bazy")

    connection.close()


def get_file_from_db(name):
    connection = sqlite3.Connection("CMS_REPO.sqlite")
    cursor = connection.cursor()
    cursor.execute("""SELECT file, type FROM FILES WHERE name = ?""", (name,))
    result = cursor.fetchall()
    connection.close()
    try:
        return (result[0][0], result[0][1])
    except:
        return "False"


def count_files_by_name(name):
    connection = sqlite3.Connection("CMS_REPO.sqlite")
    cursor = connection.cursor()
    cursor.execute("""SELECT COUNT(*) FROM FILES WHERE name = ?""", (name,))
    result = cursor.fetchall()
    connection.close()
    try:
        return result[0][0]
    except:
        return False


def get_data_json():
    return get_file_from_db("data.json")[0]


class MenuForm(Form):
    menuRadio = RadioField('Menu', choices=[('ver', 'vertical'), ('hor', 'horizontal')])


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Qwerty123!'
flask_cors.CORS(app)
repo_init()


@app.route("/data")
def return_json():
    return get_data_json()


@app.route("/data/update", methods=["POST"])
def update_data():
    files = request.files
    file = files.get('file')
    try:
        update_file_in_repo("data.json", "json", file.read())
        return Response(status=200)
    except Exception as ex:
        return Response(status=500)


@app.route("/article/update", methods=["POST"])
def update_article():
    files = request.files
    file = files.get('file')
    href = request.args["href"]
    name = f"article/{href}"
    print(href)
    try:
        if count_files_by_name(name) == 0:
            save_file_to_repo(name, "json", file.read())
        else:
            update_file_in_repo(name, "json", file.read())
        return Response(status=200)
    except:
        return Response(status=500)


@app.route("/article/get", methods
=["GET", "POST"])
def get_article():
    href = request.args["href"]
    print(href)
    try:
        res = get_file_from_db(f"article/{href}")
        if res == "False":
            0 / 0
        return res
    except:
        print("NI MO!")
        return Response(status=202)


@app.route("/gfx", methods=["GET", "POST"])
def return_gfx():
    name = request.args["name"]
    return get_file_from_db(name)


@app.route("/gfx/get", methods=["GET", "POST"])
def return_gfx2():
    print(request.get_json())

    name = request.form["name"]
    return get_file_from_db(name)


@app.route("/gfx/insert", methods=["GET", "POST"])
def insert_gfx():
    name = request.args['name']
    files = request.files
    file = files.get('file')
    try:
        if count_files_by_name(name) == 0:
            save_file_to_repo(name, "photo", file.read())
        else:
            update_file_in_repo(name, "photo", file.read())
        return Response(status=200)
    except Exception as ex:
        return Response(status=500)


boostrap = Bootstrap(app)
links = []


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
    link = [text, href]
    links.append(link)
    return render_template('formResults.html', links=links, action="clearLinks")


@app.route("/clearLinks")
def clearLinks():
    global links
    links = []
    return render_template('formResults.html', links=links, action="clearLinks")


@app.route('/registerTemplate')
def registerTemplate():
    return render_template('loginTemplate.html', label="Register", action="registerCheck")

inBase = True

@app.route('/loginCheck')
def loginCheck():
    login = request.args.get("login")
    if (inBase):
        if (login == "admin"):
            return render_template('homePage.html')
        return render_template('404.html')
    else:
        return render_template('500.html')


# tu jesli jest to nie dodaje
@app.route('/registerCheck')
def registerCheck():
    if (inBase):
        return render_template('500.html')
    else:
        return render_template('404.html')


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
    submit = SubmitField('Zaloguj')


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
    return render_template('loginForm.html', headerOne="Zaloguj się", form=form, action="/loginServiceController",
                           title="logowanie",
                           desc="Podaj dane do logowania", info=info)


@app.route('/register')
def register():
    form = userForm()
    info = ""
    if 'info' in session:
        info = session['info']
        session['info'] = ''
    return render_template('loginForm.html', headerOne="Zarejestruj się", form=form,
                           action="/registerServiceController",
                           title="rejestrowanie",
                           desc="Podaj nowy login i hasło  użytkownika", info=info)


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


@app.route('/registerServiceSite', methods=["POST"])
def registerServiceSite():
    login = request.form['login']
    passwd = request.form['passwd']
    session = {}
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
        session['status'] = 200
        return session
    except:
        session['status'] = 400
        session['info'] = "Nie udało się utworzyć użytkownika. Spróbuj zmienić login"
        return session


@app.route("/updateUserSite", methods=["GET", "POST"])
def editDataSite():
    login = request.form['login']
    loginOld = request.form['loginOld']
    passwd = request.form['passwd']
    session = {}
    try:
        loginCursor.execute(f"SELECT * from '{DBASE}' WHERE LOGIN = '{login}'")
        r = loginCursor.fetchall()
        if (len(r) != 0 and login != loginOld):
            0 / 0
        session['login'] = login
        session['passwd'] = passwd
        session['status'] = 200
        session['info'] = "zaaktualizowano pomyślnie dane"
        loginCursor.execute(f"UPDATE {DBASE} SET LOGIN ='{login}', PASSWD = '{passwd}' WHERE LOGIN = '{loginOld}'")
        loginConnector.commit()
    except:
        session['info'] = "Wystąpił błąd, Spróbuj wybrać inny login"
        session['status'] = 400
    finally:
        return session


@app.route('/loginServiceSite', methods=["POST"])
def loginServiceSite():
    login = request.form['login']
    passwd = request.form['passwd']
    session = {}
    if (login == "admin" and passwd == "admin"):
        session['login'] = login
        session['passwd'] = passwd
        session['admin'] = True
        session['status'] = 1000
        return session

    loginCursor.execute(f"SELECT * FROM '{DBASE}' WHERE LOGIN = '{login}' AND PASSWD = '{passwd}'")
    sqlRes = loginCursor.fetchall()

    if (len(sqlRes) == 1):
        session['login'] = login
        session['passwd'] = passwd
        session['status'] = 200
        return session
    else:
        session['info'] = "Niepoprawny login lub hasło"
        session['status'] = 400
        return session


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internalServerError(error):
    return render_template('500.html', title='500'), 500


if __name__ == '__main__':
    app.run(debug=True)
