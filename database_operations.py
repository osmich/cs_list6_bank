import sys, random, string
import MySQLdb
from flask import request

def register_user(param):
    conn = None

    try:
        conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')

        sql = "insert into users (FirstName, LastName, Email, UserName, City, Address, Password) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (param['firstname'] , param['lastname'], param['email'], param['username'], param['city'], param['address'], param['password'] )
                       
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        conn.commit()

    except MySQLdb.Error as e:
        print('error {}: {}'.format(e.args[0], e.args[1])) 
        return False  

    finally:
        if conn:
            conn.close()
            return True


def login_user(param):
    conn = None

    try:
        # print(param['username'])
        sql = "SELECT id FROM users WHERE UserName = \'{}\' AND Password = \'{}\'".format(param['username'], param['password'])
        # print(sql)         
        conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()
        # conn.close()

        print("rows: ", rows)
        if len(rows) == 1:
            print("yess")
            return {"result":True, "value":rows}

        return {"result":False, "value":"empty"}

    except MySQLdb.Error as e:
        print('error {}: {}'.format(e.args[0], e.args[1]))
        # conn.close()
        return {"result":False, "value":"empty"}

    finally:
        conn.close()


def new_transfer(param, user):
    sql = "insert into transfers (UserID, pln, pln_c, AccountNumber, FirstName, LastName, City, Address, TitleTransfer) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (user , param.get('PLN'), param.get('PLN_C'), param.get('accountnumber'), param.get('firstname'), param.get('lastname'), param.get('city'), param.get('address'), param.get('titletransfer') )
    try:
        conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        conn.commit()

        return True

    except MySQLdb.Error as e:
        print('error {}: {}'.format(e.args[0], e.args[1]))
        # conn.close()
        return False

    finally:
        conn.close()      

def get_transfers(user):
    sql = "SELECT * FROM transfers WHERE userID = \'{}\'".format(user)
    try:
        conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()

        return rows

    except MySQLdb.Error as e:
        print('error {}: {}'.format(e.args[0], e.args[1]))
        # conn.close()
        return None

    finally:
        conn.close()

def reset_password(user):
    sql = "SELECT Email FROM users WHERE UserName = \'{}\'".format(user)
    try:
        conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        rows = cursor.fetchall()

        if len(rows) != 1:
            return {"result":False, "value":"empty"}

        email = rows[0]["Email"]
        newPassword = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

        sql = "UPDATE users SET Password = \'{}\' WHERE UserName = \'{}\';".format(newPassword, user)
        cursor.execute(sql)
        conn.commit()

        return {"result":True, "email":email, "password":newPassword}

    except MySQLdb.Error as e:
        print('error {}: {}'.format(e.args[0], e.args[1]))
        # conn.close()
        return {"result":False, "value":"empty"}

    finally:
        conn.close()