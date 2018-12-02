from flask import (
    Flask,
    render_template,
    redirect, url_for, request,
    session
)
import os, datetime
from database_operations import register_user, login_user, get_transfers, new_transfer, reset_password
from helpers import check_keys, check_login, check_transfer, send_password


app = Flask(__name__, template_folder="templates")
app.secret_key = os.urandom(987) 

def verifyUser(sse):
    if 'user' in sse:
        return True
    return False


@app.route('/')
def home():
    session.pop('user', None)
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session.pop('user', None)
    if request.method == 'POST' and check_login(request.form):
        result = login_user(request.form)
        if result["result"] == True:
            print(result)
            print(result["value"][0]["id"])
            session['user'] = result["value"][0]["id"]
            return render_template('account.html')
    return render_template('index.html', error=error)

@app.route('/postRegister', methods=['GET', 'POST'])
def postRegister():
    if request.method == 'POST' and check_keys(request.form) and register_user(request.form):
        return render_template('postRegister.html', error=None)

    return render_template('errorRegister.html', error=None)


@app.route('/account', methods=['GET', 'POST'])
def account():
    if verifyUser(session):
        return render_template('account.html')
    return redirect('login')

@app.route('/logout')
def logout():
    if verifyUser(session):
        session.pop('user')
    return render_template('index.html')


@app.route('/form')
def form():
    if verifyUser(session):
        return render_template('form.html')
    return render_template('index.html')

@app.route('/cform', methods=['GET', 'POST'])
def cform():
    if verifyUser(session):
        return render_template('cform.html')
    return render_template('badRequest.html')

@app.route('/sendtransfer', methods=['GET', 'POST'])
def sendTransfer():
    print("-----------")
    print(request.args.get('firstname'))
    if verifyUser(session):# and check_transfer(request.args): #and request.method == 'POST'
        result = new_transfer(request.args, session['user'])
        if result == True:
            return render_template('sendTransfer.html')
        else:
            return render_template('errorForm.html')
    return render_template('badRequest.html')

@app.route('/history')
def history():
    if verifyUser(session):
        transfers = get_transfers(session["user"])
        return render_template("history.html", data=transfers)
    return render_template("index.html")

@app.route('/reset')
def reset():
    if verifyUser(session):
        session.pop('user')
    return render_template('reset.html')

@app.route('/creset', methods=['GET', 'POST'])
def creset():
    if verifyUser(session):
        session.pop('user')
    if 'user' in request.form:
        result = reset_password(request.form['user'])
        if result["result"] == True:
            send_password(result["email"], result['password'])
            return render_template('creset.html')
    return render_template('badRequest.html')

@app.route('/script.js')
def script():
    return render_template("script.js")

@app.route('/violate.js')
def violate():
    return render_template("violate.js")
    
@app.route('/violate2.js')
def violate2():
    return render_template("violate2.js")

if __name__ == '__main__':
    app.run(debug=True)


