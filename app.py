from flask import Flask, request, render_template
import mysql.connector
from mysql.connector import Error

# Configuração do Flask
app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    'user': 'root',
    'password': 'Banco2024',
    'host': 'bancodb.ct628qm8yfig.us-east-2.rds.amazonaws.com',
    'port': '3306',
    'database': 'bdprojeto',
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database']
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Rota principal com formulário de cadastro
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO users (id, email) VALUES (NULL, %s)", (email,))

                connection.commit()
                return "Usuário cadastrado com sucesso!"
            except Error as e:
                print(f"Erro ao registrar usuário: {e}")
                return "Erro ao registrar usuário."
            finally:
                connection.close()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
