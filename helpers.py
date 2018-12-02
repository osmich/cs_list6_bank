import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def check_keys(smth): 
    if 'firstname' in smth and 'lastname' in smth and 'email' in smth and 'username' in smth and 'city' in smth and 'address' in smth and 'password' in smth and 'confirm_password' in smth:
        if smth['firstname'] != "" and smth['lastname'] != "" and smth['email'] != "" and smth['username'] != "" and smth['city'] != "" and smth['address'] != "" and smth['password'] != "" and smth['confirm_password'] != "":
            return True    
    return False

def check_login(smth):
    if 'username' in smth and 'password' in smth:
        return True
    else:
        return False

def check_transfer(smth):
    if 'PLN' in smth and 'PLN_C' in smth and 'accountnumber' in smth and 'firstname' in smth and 'lastname' in smth and 'city' in smth and 'address' in smth and 'titletransfer' in smth:
        return True
    return False


 
def send_password(email, passord):
    fromaddr = "tagasak@outlook.com"
    toaddr = email
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Reset Password"
    # 
    body = "Here is your new password: {}".format(passord)
    msg.attach(MIMEText(body, 'plain'))
    # 
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(fromaddr, "k3Md9Zp5")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
