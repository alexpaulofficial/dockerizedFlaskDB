from flask import Flask, request, jsonify
import json
import pymysql
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'alessio'
app.config['MYSQL_DATABASE_PASSWORD'] = 'paolucci'
app.config['MYSQL_DATABASE_DB'] = 'projcer'
app.config['MYSQL_DATABASE_HOST'] = 'db'
mysql.init_app(app)

@app.route('/')
def get_students():
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    resp = jsonify(rows)
    resp.status_code = 200

    return resp

@app.route('/deleteAll/')
def delete_all():
    #It establishes a connection to th DB (it's like create_engine)
    conn = mysql.connect()

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    #It could be change in "DELETE FROM students"
    cursor.execute("TRUNCATE students")

    body = "Everything was deleted successfully!"

    resp = jsonify(body)
    resp.status_code = 200

    return resp

@app.route('/student', methods = ['POST'])
def add_student():
    #Get the JSON from the request body
    data = request.get_json()
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    #The student is added writing directly the SQL query
    sql = ("INSERT INTO students "
              "(name, city, address) "
              "VALUES (%(name)s, %(city)s, %(address)s)")

    cursor.execute(sql, data)

    conn.commit()
    cursor.close()
    conn.close()

    resp = jsonify("Student with name " + data["name"] + " added successfully!")
    resp.status_code = 200

    return resp

@app.route('/student', methods = ['DELETE'])
def delete_student():
    try:
        data = request.get_json()
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = ("DELETE FROM students WHERE id ="+ str(data["id"]))

        cursor.execute(sql)

        body = "Student with id " + str(data["id"]) + " removed successfully!"
        if cursor.rowcount == 0:
            body = "ID incorrect"

        conn.commit()
        cursor.close()
        conn.close()


    except mysql.cursor.Error as err:
        body = str("Something went wrong: {}".format(err))

    resp = jsonify(body)
    resp.status_code = 200

    return resp

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')

