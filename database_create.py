import sys
import MySQLdb

conn = None

try:
    conn = MySQLdb.connect('localhost', 'testuser', 'xxxx', 'cs_bank')
    print('Connected...')

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('drop table if exists users')
    cursor.execute('''create table if not exists users (
                     id int unsigned not null auto_increment,
                     FirstName varchar(256) not null,
                     LastName varchar(256) not null,
                     Email varchar(256) not null,
                     UserName varchar(256) not null,
                     City varchar(256) not null,
                     Address varchar(256) not null,
                     Password varchar(256) not null,
                     Salt varchar(256) not null,
                     primary key (id)
                   )''')

    cursor.execute('drop table if exists transfers')
    cursor.execute('''create table if not exists transfers (
                     id int unsigned not null auto_increment,
                     userID int not null,
                     pln int not null,
                     pln_c varchar(2),
                     AccountNumber varchar(256) not null,
                     FirstName varchar(256),
                     LastName varchar(256),
                     City varchar(256),
                     Address varchar(256),
                     TitleTransfer varchar(256),
                     primary key (id)
                     
                   )''')
                   

    sql = "insert into users (FirstName, LastName, Email, UserName, City, Address, Password) values ('test', 'test', 'tagasak@outlook.com', 'test', 'test', 'test', 'test')"
    cursor.execute(sql)
    conn.commit()
    

except MySQLdb.Error as e:
    print('error {}: {}'.format(e.args[0], e.args[1]))  # Error code number, description
    sys.exit(1)  # Raise a SystemExit exception for cleanup, but honor finally-block

finally:
    print('finally...')
    if conn:
        # Always close the connection
        conn.close()
        print('Closed...')