from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from datetime import datetime
import os
app = Flask(__name__)

# Função para criar a tabela de chamados no banco de dados
def create_table():
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            setor TEXT,
            urgencia TEXT,
            descricao TEXT,
            data_hora DATETIME,
            resolvido INTEGER DEFAULT 0 -- Definir o valor padrão como 0 para 'resolvido'
        )
    ''')
    conn.commit()
    conn.close()



# Verificar se o banco de dados existe e criar se não existir
#if not os.path.exists('helpdesk.db'):
   # create_table()

# Rota principal
@app.route('/chamados')
def exibir_chamados():
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    # Buscar chamados em aberto (resolvido=0)
    cursor.execute('SELECT * FROM chamados WHERE resolvido=0')
    chamados_abertos = cursor.fetchall()

    # Buscar chamados concluídos (resolvido=1)
    cursor.execute('SELECT * FROM chamados WHERE resolvido=1')
    chamados_concluidos = cursor.fetchall()

    conn.close()

    return render_template('chamados.html', chamados_abertos=chamados_abertos, chamados_concluidos=chamados_concluidos)

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nome = request.form['nome']
        setor = request.form['setor']
        urgencia = request.form['urgencia']
        descricao = request.form['descricao']

        # Obter a data e hora atuais
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('helpdesk.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chamados (nome, setor, urgencia, descricao, data_hora, resolvido) VALUES (?, ?, ?, ?, ?, ?)',
                       (nome, setor, urgencia, descricao, data_hora, 0))  # Definindo 'resolvido' como 0
        conn.commit()
        conn.close()

    return render_template('index.html')

@app.route('/marcar_resolvido/<int:chamado_id>')
def marcar_resolvido(chamado_id):
    conn = sqlite3.connect('helpdesk.db')
    cursor = conn.cursor()

    # Atualizar o chamado para 'resolvido = 1'
    cursor.execute('UPDATE chamados SET resolvido=1 WHERE id=?', (chamado_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('exibir_chamados'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

