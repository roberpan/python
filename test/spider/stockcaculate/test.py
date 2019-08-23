import time,datetime
import pymysql

def connectDB():
    db=pymysql.connect(host='localhost', user='root', password='pan19900901', port=3306, db='spiders')
    return db

strtime='2019-12-30 00:00:00'
formattime=datetime.datetime.strptime(strtime, '%Y-%m-%d %H:%M:%S')
db=connectDB()
cursor=db.cursor()
for i in range(1,2):
    delta=datetime.timedelta(days=i)
    now=formattime+delta
    sql="insert into ung(date) values ('{}')".format(now)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('failed')

db.close()
