from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuração do banco de dados
DB_CONFIG = {
    "dbname": "agenda_dev",
    "user": "postgres",
    "password": "88528506",
    "host": "localhost",
    "port": 5432
}

# Inicializa o Flask
app = Flask(__name__, template_folder='../frontend/templates')

# Página inicial (Login)
@app.route('/')
def index():
    return render_template('login.html')

# Rota para verificar CPF ou CNPJ
@app.route('/verificar_cpf_cnpj', methods=['POST'])
def verificar_cpf_cnpj():
    data = request.json
    cpf_cnpj = data.get('cpf_cnpj')

    if not cpf_cnpj:
        return jsonify({"error": "CPF/CNPJ não fornecido"}), 400

    try:
        # Conexão com o banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Consulta no banco de dados
        cursor.execute("SELECT id FROM agenda.users WHERE cpf_cnpj = %s", (cpf_cnpj,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"existe": True, "user_id": user["id"]})
        else:
            return jsonify({"existe": False})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para tela de registro
@app.route('/register')
def register():
    cpf_cnpj = request.args.get('cpf_cnpj', '')
    return render_template('register.html', cpf_cnpj=cpf_cnpj)

# Alimentar dados de cadastro
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    data = request.json
    cpf_cnpj = data.get('cpf_cnpj')
    email = data.get('email')
    telefone = data.get('telefone')
    senha = data.get('senha')

    if not all([cpf_cnpj, email, telefone, senha]):
        return jsonify({"error": "Dados incompletos"}), 400

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO agenda.users (cpf_cnpj, email, phone, password_hash) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')))",
            (cpf_cnpj, email, telefone, senha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
