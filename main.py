from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Conectar ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="funcionarios_flask"
)

cursor = db.cursor()


# Rota para criar um novo registro
@app.route('/funcionarios', methods=['POST'])
def create_record():
    data = request.get_json()
    name = data['name']
    email = data['email']

    sql = "INSERT INTO funcionarios (name, email) VALUES (%s, %s)"
    val = (name, email)

    cursor.execute(sql, val)
    db.commit()

    return jsonify({"message": "Registro criado com sucesso!"})


# Rota para ler registros
@app.route('/funcionarios', methods=['GET'])
def read_records():
    cursor.execute("SELECT * FROM funcionarios")
    records = cursor.fetchall()
    user_list = []
    for record in records:
        user = {"id": record[0], "name": record[1], "email": record[2]}
        user_list.append(user)
    return jsonify(user_list)


# Rota para atualizar um registro
@app.route('/funcionarios/<int:user_id>', methods=['PUT'])
def update_record(user_id):
    data = request.get_json()
    new_name = data['name']

    sql = "UPDATE funcionarios SET name = %s WHERE id = %s"
    val = (new_name, user_id)

    cursor.execute(sql, val)
    db.commit()

    return jsonify({"message": "Registro atualizado com sucesso!"})


# Rota para deletar um registro
@app.route('/funcionarios/<int:user_id>', methods=['DELETE'])
def delete_record(user_id):
    sql = "DELETE FROM funcionarios WHERE id = %s"
    val = (user_id,)

    cursor.execute(sql, val)
    db.commit()

    return jsonify({"message": "Registro deletado com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)
