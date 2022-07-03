import pymysql

connect = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='980729')
cursor = connect.cursor()
cursor.execute("show databases")
fetchall = cursor.fetchall()
print(fetchall)
connect.close()
