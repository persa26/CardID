import pymysql
import requests
from app import app
from db_config import mysql
from flask import render_template, flash, request, jsonify
from models.student import Students
from models.group import Groups
from models.groupstudents import GroupStudents

@app.route('/', methods=['GET'])
def add_student():
   return render_template("view.html",datas=fetchListOfStudents())

@app.route('/data', methods=['GET'])	  
def serve_data():
  rfid = request.args.get('rfid')
  if rfid:
    data = fetchListOfStudentsByUID(rfid)
    if not data:
      return jsonify({'error': 'No data found'}), 404
  else:
    data = fetchListOfStudents()
  return jsonify(data)

@app.route("/add", methods=["POST"])
def home():
 try:
   _id=request.form.get('id')
   _name=request.form.get('name')
   _surname=request.form.get('surname')
   _email=request.form.get('mail')
   _rfid=request.form.get('rfid')
   sql = "INSERT INTO student(id, name, surname, mail, rfid) VALUES(%s, %s, %s, %s, %s)"
   data = (_id, _name, _surname,_email, _rfid)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute(sql, data)
   conn.commit()
   return render_template('view.html',datas=fetchListOfStudents())
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

@app.route('/deleteStudent', methods=['POST'])
def deleteStudent():
 try:
   _id=request.form.get('id')
   print(_id)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("DELETE FROM Students WHERE id=%s", (_id))
   conn.commit()
   return render_template('view.html',datas=fetchListOfStudents())
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()


def fetchListOfStudents():
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM Students")
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

def fetchListOfStudentsByUID(rfid):
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM Students WHERE rfid=%s", (rfid))
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()


def fetchGroupFromStudentId(studentId):
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM GroupStudents WHERE studentId=%s", (studentId))
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

def fetchGroupById(groupId):
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM `Groups` WHERE id=%s", (groupId))
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

@app.route('/studentUpdate', methods=['POST'])
def update_student():
 try:
   _id=request.form.get('id')
   _name=request.form.get('uname')
   _surname=request.form.get('usurname')
   _mail=request.form.get('umail')
   _rfid=request.form.get('urfid')
  
   sql = "UPDATE Students SET name=%s, surname=%s, mail=%s, rfid=%s WHERE id=%s"
   data = (_name, _surname, _mail, _rfid, _id,)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute(sql, data)
   conn.commit()
   return render_template('view.html',datas=fetchListOfStudents())
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()

@app.route('/update-from-external', methods=['GET'])
def update_data():
    response = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')
    if response.status_code == 200:
        data = response.json()
        # Procesar los datos y actualizar la base de datos
        # ...
        # return jsonify({'success': 'Data updated'})
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data'}), 500

@app.route('/students')
def get_students():
    students = Students.query.all()
    return jsonify([e.serialize() for e in students])

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")


@app.route('/groupofstudent/<studentId>')
def fromStudentIdToGroupName(studentId):
  # group = GroupStudents.query.filter_by(id=studentId).first()
  group = fetchGroupFromStudentId(studentId)
  print(group)
  if group:
    groupId = group[0]['groupId']
    # groupName = Groups.query.filter_by(id=groupId).first()
    groupName = fetchGroupById(groupId)
    if groupName:
      return groupName[0]['name']
  return "No group"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')