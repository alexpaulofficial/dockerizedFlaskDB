import time
import json
from sqlalchemy import select, create_engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# PostgreSQL configurations
DBUSER = 'alessio'
DBPASS = 'paolucci'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'projcer'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)

db = SQLAlchemy(app)

# Students model
class students(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    address = db.Column(db.String(200))

    def __init__(self, name, city, address):
        self.name = name
        self.city = city
        self.address = address

# Function for initialization of the database
def database_initialization_sequence():
    #db.create_all()
    #It's only a test, at the end it's removed from the DB
    test = students(
            'Alessio',
            'Jesi',
            'Via Jesi 1')
    db.session.add(test)
    db.session.rollback()
    db.session.commit()

@app.route('/')
def get_students():
    #The engine establishes a connection to th DB (it's like mysql.connect())
    engine = create_engine('postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
                                   user=DBUSER,
                                   passwd=DBPASS,
                                   host=DBHOST,
                                   port=DBPORT,
                                   db=DBNAME))

    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")

    rows = cursor.fetchall()

    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close()
    conn.close()
    return resp

@app.route('/deleteAll')
def delete_all():
    engine = create_engine('postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
                                   user=DBUSER,
                                   passwd=DBPASS,
                                   host=DBHOST,
                                   port=DBPORT,
                                   db=DBNAME))

    conn = engine.raw_connection()
    cursor = conn.cursor()
    #It could be change in "DELETE FROM students"
    cursor.execute("TRUNCATE students")

    conn.commit()
    body = "Everything was deleted successfully!"
    #Check if everything is really deleted
    if cursor.rowcount == 0:
            body = "ID incorrect"
    cursor.close()
    conn.close()
    return jsonify(body)

@app.route('/student', methods=['POST'])
def add_student():
    #Get the JSON from the request body
    data = request.get_json()
    #The model class is used to create and add a student (without writing down the SQL query)
    student = students(
        data['name'],
        data['city'],
        data['address'])

    db.session.add(student)
    db.session.commit()

    resp = jsonify("Student with name " + data["name"] + " added successfully!")
    resp.status_code = 200

    return resp

@app.route('/studentDelete', methods = ['POST'])
def delete_student():
    data = request.get_json()
    engine = create_engine('postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
                                       user=DBUSER,
                                       passwd=DBPASS,
                                       host=DBHOST,
                                       port=DBPORT,
                                       db=DBNAME))

    conn = engine.raw_connection()
    cursor = conn.cursor()

    sql = ("DELETE FROM students WHERE id ="+ str(data["id"]))

    cursor.execute(sql)

    body = "Student with id " + str(data["id"]) + " removed successfully!"
    if cursor.rowcount == 0:
        body = "ID incorrect"

    conn.commit()
    cursor.close()
    conn.close()

    resp = jsonify(body)
    resp.status_code = 200

    return resp

if __name__ == '__main__':
    dbstatus = False
    #When the app starts it controls if the database exists, otherwise it creates it
    while dbstatus == False:
        try:
            db.create_all()
        except:
            time.sleep(2)
        else:
            dbstatus = True
    database_initialization_sequence()
    app.run(debug=True, host='0.0.0.0')
