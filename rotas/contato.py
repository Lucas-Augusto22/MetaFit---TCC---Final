from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db_connection
import psycopg2

bp = Blueprint('contato', __name__)


@bp.route('/contact', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        # Coletar dados do formulário
        primeiro_nome = request.form.get('fname')
        ultimo_nome = request.form.get('lname')
        email = request.form.get('email')
        assunto = request.form.get('subject')
        mensagem = request.form.get('message')

        # Validar campos obrigatórios
        if not primeiro_nome or not ultimo_nome or not email or not assunto or not mensagem:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
            return render_template('contact.html')

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Verificar se o email existe na tabela de usuários
            cur.execute(
                'SELECT id_cadastro FROM cadastrousuarios WHERE email_usuario = %s',
                (email,)
            )
            usuario = cur.fetchone()

            if usuario:
                id_cadastro = usuario[0]
            else:
                # Se o usuário não existe, criar um registro temporário ou usar NULL
                # Vou usar NULL para manter a integridade referencial
                id_cadastro = None

            # Inserir na tabela contato
            cur.execute(
                '''INSERT INTO contato 
                (id_cadastro, assunto_contato, mensagem_contato) 
                VALUES (%s, %s, %s)''',
                (id_cadastro, assunto, mensagem)
            )

            conn.commit()
            cur.close()
            conn.close()

            flash('Mensagem enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('contato.contato'))

        except psycopg2.Error as e:
            print(f"Erro ao salvar contato: {str(e)}")
            flash('Erro ao enviar mensagem. Tente novamente.', 'error')
            return render_template('contact.html')
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            flash('Erro inesperado. Tente novamente.', 'error')
            return render_template('contact.html')

    # Se for GET, apenas renderiza o template
    return render_template('contact.html')