from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração da conexão com o banco de dados MySQL
db = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# Criar cursor para executar queries
cursor = db.cursor()

# Rota Principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para Página de Criação
@app.route('/criar')
def pagina_criar():
    return render_template('criar.html')

# Rota para Criar Livro
@app.route('/criar/novo', methods=['POST'])
def criar_livro():
    titulo = request.form['titulo']
    ano_publicacao = request.form['ano_publicacao']
    editora = request.form['editora']
    isbn = request.form['isbn']
    
    query = "INSERT INTO livro (titulo, ano_publicacao, editora, isbn) VALUES (%s, %s, %s, %s)"
    values = (titulo, ano_publicacao, editora, isbn)
    
    cursor.execute(query, values)
    db.commit()
    
    return redirect(url_for('index'))

# Rota para Listar Livros
@app.route('/listar')
def listar():
    cursor.execute("SELECT * FROM livro")
    # Pegando os nomes das colunas
    colunas = [desc[0] for desc in cursor.description]
    # Convertendo os resultados em dicionários
    livros = [dict(zip(colunas, livro)) for livro in cursor.fetchall()]
    return render_template('listar.html', livros=livros)

# Rota para Página de Edição
@app.route('/editar/<int:id>')
def pagina_editar(id):
    cursor.execute("SELECT * FROM livro WHERE id = %s", (id,))
    # Pegando os nomes das colunas
    colunas = [desc[0] for desc in cursor.description]
    # Convertendo o resultado em dicionário
    livro_tupla = cursor.fetchone()
    if livro_tupla:
        livro = dict(zip(colunas, livro_tupla))
    else:
        return "Livro não encontrado", 404
    return render_template('editar.html', livro=livro)

# Rota para Editar Livro
@app.route('/editar/salvar/<int:id>', methods=['POST'])
def editar_livro(id):
    titulo = request.form['titulo']
    ano_publicacao = request.form['ano_publicacao']
    editora = request.form['editora']
    isbn = request.form['isbn']
    
    query = "UPDATE livro SET titulo = %s, ano_publicacao = %s, editora = %s, isbn = %s WHERE id = %s"
    values = (titulo, ano_publicacao, editora, isbn, id)
    
    cursor.execute(query, values)
    db.commit()
    
    return redirect(url_for('listar'))

# Rota para Deletar Livro
@app.route('/deletar/<int:id>')
def deletar(id):
    cursor.execute("DELETE FROM livro WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('listar'))

# Inialização do Servidor
if __name__ == '__main__':
    app.run(debug=True)