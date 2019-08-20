import pymysql

def connect():
    db=pymysql.connect(host='localhost', user='root', password='pan19900901', port=3306, db='spiders')
    return db
