import pymysql
import requests
from app import app
from db_config import mysql
from flask import render_template
from flask import flash, request, jsonify

@app.route('/', methods=['GET'])
def add_employee():
   return render_template("view.html",datas=fetchListOfEmployees())

@app.route('/data', methods=['GET'])	  
def serve_data():
  rfid = request.args.get('rfid')
  if rfid:
    data = fetchListOfEmployeesByEmail(rfid)
    if not data:
      return jsonify({'error': 'No data found'}), 404
  else:
    data = fetchListOfEmployees()
  return jsonify(data)

@app.route("/add", methods=["POST"])
def home():
 try:
   _id=request.form.get('id')
   _name=request.form.get('uname')
   _email=request.form.get('email')
   _salary=request.form.get('salary')
   sql = "INSERT INTO employee(id, uname, email,salary) VALUES(%s, %s, %s ,  %s)"
   data = (_id, _name, _email,_salary)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute(sql, data)
   conn.commit()
   return render_template('view.html',datas=fetchListOfEmployees())
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

@app.route('/deleteEmployee', methods=['POST'])
def deleteEmployee():
 try:
   _id=request.form.get('id')
   print(_id)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute("DELETE FROM employee WHERE id=%s", (_id))
   conn.commit()
   return render_template('view.html',datas=fetchListOfEmployees())
 except Exception as e:
  print(e)
 finally:
  cursor.close() 
  conn.close()


def fetchListOfEmployees():
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM employee")
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()


def fetchListOfEmployeesByEmail(rfid):
 try:
   conn = mysql.connect()
   cursor = conn.cursor(pymysql.cursors.DictCursor)
   cursor.execute("SELECT * FROM employee WHERE email=%s", (rfid))
   rows = cursor.fetchall()
   return rows
 except Exception as e:
   print(e)
 finally:
   cursor.close() 
   conn.close()

@app.route('/employeeUpdate', methods=['POST'])
def update_employee():
 try:
   _id=request.form.get('id')
   _name=request.form.get('uname')
   _email=request.form.get('email')
   _salary=request.form.get('salary')
  
   sql = "UPDATE employee SET uname=%s, email=%s, salary=%s WHERE id=%s"
   data = (_name, _email, _salary, _id,)
   conn = mysql.connect()
   cursor = conn.cursor()
   cursor.execute(sql, data)
   conn.commit()
   return render_template('view.html',datas=fetchListOfEmployees())
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080')