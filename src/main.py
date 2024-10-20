from flask import Flask, jsonify, request
from db import get_db_connection
from auth.auth import check_api_key

app = Flask(__name__)


@app.route('/locales', methods=['POST'])
def create_local():
    check_api_key()  
    data = request.json
    name = data.get('Name')
    creation_date = data.get('Creation_Date')
    phone = data.get('Phone')
    street_name = data.get('Street_Name')
    street_number = data.get('Street_Number')
    neighborhood_name = data.get('Neighborhood_Name')
    district_name = data.get('District_Name')
    cap_code = data.get('CAP_Code')

    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("""
        INSERT INTO locales (Name, Creation_Date, Phone) 
        VALUES (%s, %s, %s)
    """, (name, creation_date, phone))
    local_id = cursor.lastrowid

    
    cursor.execute("""
        INSERT INTO direcciones (LocalName, Street_Name, Street_Number, Neighborhood_Name, District_Name, CAP_Code) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, street_name, street_number, neighborhood_name, district_name, cap_code))
    db.commit()

    cursor.close()
    db.close()
    
    return jsonify({"ID": local_id}), 201

@app.route('/locales/<int:id>', methods=['PUT'])
def update_local(id):
    check_api_key()  
    data = request.json
    name = data.get('Name')
    creation_date = data.get('Creation_Date')
    phone = data.get('Phone')
    street_name = data.get('Street_Name')
    street_number = data.get('Street_Number')
    neighborhood_name = data.get('Neighborhood_Name')
    district_name = data.get('District_Name')
    cap_code = data.get('CAP_Code')

    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("""
        UPDATE locales 
        SET Name = %s, Creation_Date = %s, Phone = %s 
        WHERE ID = %s
    """, (name, creation_date, phone, id))

    
    cursor.execute("""
        UPDATE direcciones 
        SET LocalName = %s, Street_Name = %s, Street_Number = %s, Neighborhood_Name = %s, District_Name = %s, CAP_Code = %s
        WHERE LocalName = %s
    """, (name, street_name, street_number, neighborhood_name, district_name, cap_code, name))

    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({"message": "Local actualizado"}), 200

@app.route('/locales/<int:id>', methods=['DELETE'])
def delete_local(id):
    check_api_key()  
    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("SELECT Name FROM locales WHERE ID = %s", (id,))
    local = cursor.fetchone()
    if not local:
        return jsonify({"error": "Local no encontrado"}), 404
    
    local_name = local[0]

    
    cursor.execute("DELETE FROM direcciones WHERE LocalName = %s", (local_name,))
    
    
    cursor.execute("DELETE FROM locales WHERE ID = %s", (id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Local y dirección eliminados"}), 200


@app.route('/events', methods=['POST'])
def create_event():
    check_api_key()  
    data = request.json
    name = data.get('Name')
    creation_date = data.get('Creation_Date')
    phone = data.get('Phone')
    type_local = data.get('Type_Local')
    street_name = data.get('Street_Name')
    street_number = data.get('Street_Number')
    neighborhood_name = data.get('Neighborhood_Name')
    district_name = data.get('District_Name')
    cap_code = data.get('CAP_Code')

    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("""
        INSERT INTO events (Name, Creation_Date, Phone, Type_Local) 
        VALUES (%s, %s, %s, %s)
    """, (name, creation_date, phone, type_local))
    event_id = cursor.lastrowid

    
    cursor.execute("""
        INSERT INTO direcciones (EventName, Street_Name, Street_Number, Neighborhood_Name, District_Name, CAP_Code) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, street_name, street_number, neighborhood_name, district_name, cap_code))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"ID": event_id}), 201

@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    check_api_key()  
    data = request.json
    name = data.get('Name')
    creation_date = data.get('Creation_Date')
    phone = data.get('Phone')
    type_local = data.get('Type_Local')
    street_name = data.get('Street_Name')
    street_number = data.get('Street_Number')
    neighborhood_name = data.get('Neighborhood_Name')
    district_name = data.get('District_Name')
    cap_code = data.get('CAP_Code')

    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("""
        UPDATE events 
        SET Name = %s, Creation_Date = %s, Phone = %s, Type_Local = %s 
        WHERE ID = %s
    """, (name, creation_date, phone, type_local, id))

    
    cursor.execute("""
        UPDATE direcciones 
        SET EventName = %s, Street_Name = %s, Street_Number = %s, Neighborhood_Name = %s, District_Name = %s, CAP_Code = %s
        WHERE EventName = %s
    """, (name, street_name, street_number, neighborhood_name, district_name, cap_code, name))

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Evento actualizado"}), 200

@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    check_api_key()  
    db = get_db_connection()
    cursor = db.cursor()

    
    cursor.execute("SELECT Name FROM events WHERE ID = %s", (id,))
    event = cursor.fetchone()
    if not event:
        return jsonify({"error": "Evento no encontrado"}), 404

    event_name = event[0]

    
    cursor.execute("DELETE FROM direcciones WHERE EventName = %s", (event_name,))

    
    cursor.execute("DELETE FROM events WHERE ID = %s", (id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Evento y dirección eliminados"}), 200


@app.route('/locales/barrio/<string:barrio>', methods=['GET'])
def get_locales_by_neighborhood(barrio):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT l.* FROM locales l 
        INNER JOIN direcciones d ON l.ID = d.ID 
        WHERE d.Neighborhood_Name LIKE %s
    """, ('%' + barrio + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontraron locales en ese barrio"}), 404
    return jsonify(result), 200

@app.route('/locales/nombre/<string:nombre>', methods=['GET'])
def get_locales_by_name(nombre):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM locales WHERE Name LIKE %s", ('%' + nombre + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontraron locales con ese nombre"}), 404
    return jsonify(result), 200

@app.route('/locales/telefono/<string:nombre>', methods=['GET'])
def get_local_phone_by_name(nombre):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT Phone FROM locales WHERE Name = %s", (nombre,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontró el teléfono del local"}), 404
    return jsonify({"Telefono": result[0]}), 200

@app.route('/locales/distrito/<string:distrito>', methods=['GET'])
def get_locales_by_district(distrito):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT l.* FROM locales l 
        INNER JOIN direcciones d ON l.ID = d.ID 
        WHERE d.District_Name LIKE %s
    """, ('%' + distrito + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontraron locales en ese distrito"}), 404
    return jsonify(result), 200


@app.route('/events/barrio/<string:barrio>', methods=['GET'])
def get_events_by_neighborhood(barrio):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT e.* FROM events e 
        INNER JOIN direcciones d ON e.ID = d.ID 
        WHERE d.Neighborhood_Name LIKE %s
    """, ('%' + barrio + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontraron eventos en ese barrio"}), 404
    return jsonify(result), 200

@app.route('/events/nombre/<string:nombre>', methods=['GET'])
def get_events_by_name(nombre):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM events WHERE Name LIKE %s", ('%' + nombre + '%',))
    result = cursor.fetchall()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontraron eventos con ese nombre"}), 404
    return jsonify(result), 200

@app.route('/events/telefono/<string:nombre>', methods=['GET'])
def get_event_phone_by_name(nombre):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT Phone FROM events WHERE Name = %s", (nombre,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if not result:
        return jsonify({"error": "No se encontró el teléfono del evento"}), 404
    return jsonify({"Telefono": result[0]}), 200


if __name__ == '__main__':
    app.run(debug=True)
