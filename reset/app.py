from flask import Flask, render_template, redirect, url_for, flash, request, make_response
import pyad.adquery
import pyad.aduser
import jwt
from ldap3 import Server, Connection, ALL, NTLM
from functools import wraps
import pythoncom


dc = '192.168.66.5'
domain = "lab.com"
# user = "Administrator"
# password = "Bubiman10!"


def check_password(dc, domain, user, password):
    server = Server(dc, get_info=ALL)
    try:
        with Connection(server, user='{}\\{}'.format(domain, user), password=password, authentication=NTLM) as conn:
            if conn.bind():
                return True
    except:
        return False


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'


def get_user_from_token():
    user = None
    if "access_token" in request.cookies:
        token = dict(request.cookies)["access_token"]
        payload = jwt.decode(
            token, app.config["SECRET_KEY"], algorithms="HS256")
        if "user" in payload:
            user = payload["user"]
    return user


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_user_from_token()
        if user is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrapper


@app.route('/', methods=['GET', 'POST'])
def index():
    global dc, domain
    pythoncom.CoInitialize()
    if request.method == "GET":
            response = make_response(render_template('index.html'))
            response.set_cookie('access_token', "")
            return response
    else:
        username = request.form.get("username")
        password = request.form.get("password")

        check = check_password(dc, domain, username, password)
        if check:
            flash("Login Success", "success")
            encoded = jwt.encode({"user": username},
                                 app.config["SECRET_KEY"], algorithm="HS256")
            response = make_response(redirect(url_for('change_password')))
            response.set_cookie('access_token', encoded)
            return response
        else:
            flash("Invalid Credentials", "error")
        return redirect(url_for('index'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == "GET":
        return render_template('change_password.html')
    else:
        pythoncom.CoInitialize()
        user = get_user_from_token()
        password = request.form.get("password")
        repeat = request.form.get("repeat")

        if password == repeat:
            q = pyad.adquery.ADQuery()
            q.execute_query(
                attributes=["cn"],
                where_clause="sAMAccountName = 'sdaini'",
                base_dn="CN=users,DC=lab,DC=com"
            )
            cn = None
            for row in q.get_results():
                cn = row["cn"]
                    
            ad_user = pyad.aduser.ADUser.from_cn(cn)
            try:
                ad_user.set_password(password)
                flash("Password Updated", "success")
                response = make_response(redirect(url_for('index')))
                return response
            except Exception as e:
                flash("Error", "error")
                return render_template('change_password.html')
        else:
            flash("Password must be equal", "error")
            return render_template('change_password.html')

if __name__ == '__main__':
    app.run()
