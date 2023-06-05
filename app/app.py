import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def save_data():
    data = request.get_json()  # Obtener el cuerpo de la petición en formato JSON
    with open('data.json', 'w') as file:
        file.write(json.dumps(data))
    return 'Data saved successfully'

@app.route('/rfid/<string:rfid>', methods=['GET'])
def read_data(rfid):
    try:
        with open('data.json', 'r') as file:
            lines = file.readlines()
            json_content = ''.join(lines)  # Unir las líneas en una sola cadena
            data = json.loads(json_content)
            
            # Verificar si el rfid existe en el archivo JSON
            for student in data['students']:
                if student['rfid'] == rfid:
                    # Realizar la petición GET al servidor externo
                    response = requests.get(f"http://localhost:3080/api/v1/students/{student['id']}/locations/{data['location']['locationId']}/access/rfid")
                    return response.json()
                    # return jsonify(student)
            return 'RFID not found'
    except FileNotFoundError:
        return 'File not found'

if __name__ == '__main__':
    app.run()